#include <mpi.h>
#include <stdlib.h>
#include <stdio.h>
#include <regex.h>
#include <sys/types.h>
#include <dirent.h>
#include <string.h>
#include "parsefiles.h"
//TODO: delete non-used includes

//TODO:Use proper int datatypes to prevent weird multi processor stuff
//one solution is to use left shifts in a 64_bit int, which should eventually make it so

#define HTDIRECT "../htpages/"

#define DIETAG 2
void master(int n);
void slave();
int main(int argc, char **argv) {
  MPI_Init(&argc, &argv);
  int myrank,nproc;
  MPI_Comm_size(MPI_COMM_WORLD,&nproc);
  MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
  //nproc=0;
  //myrank=0;
  if (myrank) slave(myrank);
  else master(nproc);
  MPI_Finalize();
  
}
void master(int n) {
  //opene file's and stuff
  int rank;
  DIR *dp;
  FILE *filein;
  struct dirent *ep;
  const char *dirp=HTDIRECT;//"htpages/";
  dp=opendir(dirp);
  //if (dp!=NULL) {
  //  ep=readdir(dp);
  //}
  char *fi;
  for (rank=1;rank<n && (ep=readdir(dp));rank++) {
    //get size of file
    fi=ep->d_name;
    while (fi[0]=='.') {
      ep=readdir(dp);
      fi=ep->d_name;
    }

    char *path=malloc(strlen(dirp)*sizeof(char)+strlen(fi)*sizeof(char)+sizeof(char));
    strcpy(path,dirp);
    strcat(path,fi);
    printf("FILENAME:%s\n",path);
    filein=fopen(path,"r");

    fseek(filein,0,SEEK_END);
    long siz=ftell(filein)+1;
    fseek(filein,0,SEEK_SET);
    
    char *buffer=malloc(sizeof(char)*(siz));
    char c;
    int i=0;
    while ((c=getc(filein))!=EOF){
      buffer[i]=c;
      i++;
    }

    fclose(filein);
    //printf("%s\n",buffer);
    //printf("%d\n",i);
    //send data other processor
        
    MPI_Send(&siz,1,MPI_LONG,rank,1,MPI_COMM_WORLD); //rank, after type
    
    MPI_Send(buffer,siz,MPI_CHAR,rank,1,MPI_COMM_WORLD);

    free(buffer);
    //XSfree(fi);//nowork
    free(path);
    printf("did\n");
    //increment directory
    //ep=readdir(dp);
  }
  
  FILE *fileout;
  fileout=fopen("courseresult.txt","w");
  MPI_Status status;
  while ((ep=readdir(dp))) {
    //get return
   
    char *buf;
    long siz;
    MPI_Recv(&siz,2,MPI_LONG,MPI_ANY_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD,&status);
    printf("RECIEVING from %d\n",status.MPI_SOURCE);
    buf=malloc(sizeof(char)*(siz+1));
    MPI_Recv(buf,siz,MPI_CHAR,status.MPI_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD,&status);
    fputs(buf,fileout);//fileout.write(buf);
    free(buf);
    //  siz


    fi=ep->d_name;
    while (fi[0]=='.') {
      ep=readdir(dp);
      fi=ep->d_name;
    }
    if (!ep) break;
    char *path=malloc(strlen(dirp)*sizeof(char)+strlen(fi)*sizeof(char)+sizeof(char));
    //char *path=malloc(sizeof(dirp)+sizeof(fi));
    strcpy(path,dirp);
    strcat(path,fi);
    printf("FILENAME:%s\n",path);
    filein=fopen(path,"r");
    
    fseek(filein,0,SEEK_END);
    siz=ftell(filein);
    fseek(filein,0,SEEK_SET);
    buf=malloc(sizeof(char)*siz);
    char c;
    int i=0;
    while ((c=getc(filein))!=EOF){
      buf[i]=c;
      i++;
    }
    fclose(filein);
    // printf("%s\n",buffer);
    //printf("%d\n",i);
    //send data other processor
    
    MPI_Send(&siz,1,MPI_LONG,status.MPI_SOURCE,1,MPI_COMM_WORLD);
    MPI_Send(buf,siz,MPI_CHAR,status.MPI_SOURCE,1,MPI_COMM_WORLD);
    free(buf);
    free(path);
    // ep=readdir(dp);
    }
  //finish up remaining things
   for (rank=1;rank<n;rank++) {
    //get size of file
     printf("CLEANING UP%d",rank);
    
     long siz;
     
     //FIX DATATYPE HERE
     MPI_Recv(&siz,2,MPI_LONG,rank,MPI_ANY_TAG,MPI_COMM_WORLD,&status);

     char *buffer=malloc(sizeof(char)*(siz+1));
     MPI_Recv(buffer,siz,MPI_CHAR,rank,MPI_ANY_TAG,MPI_COMM_WORLD,&status);
     fputs(buffer,fileout);
     free(buffer);

     
   }
   fclose(fileout);
   //terminiate slaves
    for (rank=1;rank<n;rank++) {
      printf("SENDING KILL %d\n",rank);
      MPI_Send(0,1,MPI_LONG,rank,DIETAG,MPI_COMM_WORLD);
    }
    closedir(dp);
    printf("QED DUNZOE\n");
    
    
}

    //send file

void slave(int num){
  //make regexes here, that way they don't have to be recompiled each time
  long siz;
  char *buffer=NULL;
  MPI_Status status;
  int Tot=0;
  while (1) {
    printf("process %d receiving siz\n",num);
    MPI_Recv(&siz,1,MPI_LONG,0,MPI_ANY_TAG,MPI_COMM_WORLD,&status);
    //if (status) printf("Error in %d\n",num);
    if (status.MPI_TAG == DIETAG) break;
    //  printf("SIZ %ld\n",siz);
    if (buffer==NULL) {
      buffer=malloc(sizeof(char)*(siz+2));
    }
    else {
      buffer=realloc(buffer,sizeof(char)*(siz+2));
    }
    printf("process %d receiving buf\n",num);
    MPI_Recv(buffer,siz,MPI_CHAR,0,MPI_ANY_TAG,MPI_COMM_WORLD,&status);
    //printf("Received Msg:\n%s",buffer);
    //if (status) printf("Error in %d\n",num);
    char *ret=parsedResult(buffer,&Tot);
    
    siz=strlen(ret)+1;
    printf("prcess %d sending out data\n",num);
    // printf("%s %lu\n",ret,siz);

    //FIX DATATYPE HERE
    MPI_Send(&siz,1,MPI_LONG,0,1,MPI_COMM_WORLD);

    MPI_Send(ret,siz,MPI_CHAR,0,1,MPI_COMM_WORLD); //former siz+1
    free(ret);
    //free(buffer);
    
  }
  printf("%d FIN\n",Tot);
  printf("dieing\n");
    
  
}
