#include "parsefiles.h"
//#include <regex.h>

//Order is :
//Title      0 X
//Season/time period  1
//Notes    X   2
//courseID(unique)   X   3
//section   X   4
//Type:Lec/Tut... X   5
//Credit Hrs   6
//link   7
//5 lines of days of week X   8 
//time period XXXX-YYYY   X   9 
//location ?   10
//MAX    11
//CUR   12 
//AVAIL  X   13
//waitlist  14
//Percent full   15
//Xlist Max  16 
//Xlist cur  17 
//Instructors various lines of   18
//tuition code  19
//tuition hrs  20


//then makes new entry with starting at Notes, skips title and season/time prd
int isBoth(char one, char two) {
  //for checking if entry is a note
  if (one>=65 && one<=90 && two >=97 && two<=122) {
    return 0;
  }
  return 1;
}
char *parsedResult(char *intext,int *Tot) {
  regex_t r,sp,crs,idreg,notreg;

  //regex strings

  //make regexes in slave function
  const char *regtext=">[^>]+<";    //">\s*(?=.*[\S])([^>]+?)\s*<";
  const char *spact=">[ \n\r\t]+<";
  const char *crdtext=">[0-9][0-9][0-9][0-9][0-9]<"; //redit number(check this)
  const char *coursenametxt=">[A-Z][A-Z][A-Z][A-Z] [0-9][0-9][0-9][0-9]";
  const char *notetext=">[A-Z][A-Z][A-Z][A-Z] [0-9][0-9][0-9][0-9]X [A-Z][A-Z]";
  //  const char *
  const char *daytxt=">[MTWRF[&nbsp;]]<";
  // const char *notetxt=">[A-Z]+";
  
  
  
  int status=regcomp(&r,regtext,REG_EXTENDED);
  const char *p=intext;
  if (status) {
    char *reg_error=malloc(400);
    printf("PICNIC IN REGEX COMPILE!!\n");
    regerror(status,&r,reg_error,400);
    printf("ERROR: %s : %s\n",regtext,reg_error);
  }
  const int n_matches=15;//some arbitrary number, should be big                                                                                                                    
  regmatch_t m[n_matches];
  regmatch_t g[n_matches];
  regmatch_t h[n_matches];
  char * finresult=calloc(20000,sizeof(char)); //allocate space
  status=regcomp(&sp,spact,REG_EXTENDED);
  if (status) {
    printf("PICNIC SPACES");
  }
  status=regcomp(&crs,coursenametxt,REG_EXTENDED);
  if (status) {
    printf("PICNIC SPACES");
  }
  status=regcomp(&idreg,crdtext,REG_EXTENDED);
  if (status) {
    printf("PICNIC SPACES");
  }
  status=regcomp(&notreg,notetext,REG_EXTENDED);
  if (status) {
    printf("PICNIC SPACES");
  }
  
  int ind=0;
  int i=0;
  char * courseName=malloc(40*sizeof(char)); //HERE
  int courseSize=0;
  
  while (1) {
    
    int offset=0;

    int nomatch=regexec(&r,p,n_matches,m,0); //problem here
    if (nomatch) {
      break;
      //return stuff                                                                                                                                                               
    }
    //for (i=0;i<n_matches;i++)                                                                                                                                                    
    int start,finish;
    //if (i==0|| 2|| 3|| 4|| 5|| 8|| 9|| 10|| 13 ){
    start=m[0].rm_so + (p - intext);
    finish = m[0].rm_eo +(p-intext);
    char * inb=calloc((finish-start+1),sizeof(char));
    memcpy(inb,intext+start,(finish-start)*sizeof(char));
    
    nomatch=regexec(&sp,inb,n_matches,g,0);
    
    if (nomatch) {
      nomatch=regexec(&crs,inb,n_matches,g,0);
      int bmatch=regexec(&notreg,inb,n_matches,g,0);
      if (!nomatch&&bmatch) {  //check for a change in course
	i=0;
	//free(courseName);
	char *tmp=realloc(courseName,sizeof(char)*(finish-start-1));
	if (tmp==NULL){
	  printf("WASSUPFNADFA\n");
	}
	courseName=tmp;
	courseName[finish-start-2]='\0';
	memcpy(courseName,intext+start+1,(finish-start-2)*sizeof(char)); //check for overflow HERE
	courseSize=finish-start-2;
	*Tot=*Tot+1;
      }
      nomatch=regexec(&idreg,inb,n_matches,h,0);
      if (!nomatch) {
	i=6;
	memcpy(finresult+ind,courseName,(courseSize)*sizeof(char)); //here
	ind+=courseSize+1;
	finresult[ind-1]=(char)255;
      }
	      
      if ( i==6 ||i==8||i==7|| i==11 || i==12 || i==13 || i==14 || i==15||i==16||i==20) {
	if (i==11&&!strcmp(inb,">C/D<")) {
	    i=16;
	}
	
	  
	memcpy(finresult+ind,intext+start+1,(finish-start-2)*sizeof(char));
	ind+=finish-start-2+1;
       finresult[ind-1]=(char)255; //seperater
       
       


      }
      //printf("%.*s %d\n",finish-start, intext+start,i);
 
	 // scan for the next new line
      for (;;offset++) {
	if (p[offset+m[0].rm_eo]=='\n') break;
      }
 
      i++;
    }

    //}
    p+=m[0].rm_eo+offset;
    
    
    free(inb);
  }
  //maybe have a compile function, and then free when all the transfers are actually done
  free(courseName);
  regfree(&r);
  regfree(&sp);
  regfree(&idreg);
  return finresult;
}

char *updateResult(char *intext) {
  regex_t r,sp;
  const char *regtext=">[^>]+<";    //">\s*(?=.*[\S])([^>]+?)\s*<";
  const char *spact="> +<";
  int status=regcomp(&r,regtext,REG_EXTENDED);
  const char *p=intext;
  if (status) {
    char *reg_error=malloc(400);
    printf("PICNIC IN REGEX COMPILE!!\n");
    regerror(status,&r,reg_error,400);
    printf("ERROR: %s : %s\n",regtext,reg_error);
  }
  const int n_matches=15;//some arbitrary number, should be big                                                                                                                    
  regmatch_t m[n_matches];
  regmatch_t g[n_matches];
  char * finresult=calloc(100,sizeof(char)); //allocate space
  status=regcomp(&sp,spact,REG_EXTENDED);
  if (status) {
    printf("PICNIC SPACES");
  }
  int ind=0;
  while (1) {
    
    
    int nomatch=regexec(&r,p,n_matches,m,0);
    if (nomatch) {
      break;
      //return stuff                                                                                                                                                               
    }
    //for (i=0;i<n_matches;i++)                                                                                                                                                    
    int start,finish;

    start=m[0].rm_so + (p - intext);
    finish = m[0].rm_eo +(p-intext);
    char * inb=calloc((finish-start+1),sizeof(char));
    memcpy(inb,intext+start,(finish-start)*sizeof(char));
    nomatch=regexec(&sp,inb,n_matches,g,0);
    printf("%.*s\n",finish-start, intext+start);
    if (nomatch) {
      memcpy(finresult+ind,intext+start+1,(finish-start-2)*sizeof(char));
      ind+=finish-start-2+1;
      finresult[ind-1]=(char)255; //seperater
    }
    
    p+=m[0].rm_eo;
    
    
    free(inb);
  }
  regfree(&r);
  regfree(&sp);
  return finresult;
}


