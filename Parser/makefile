CC= mpicc
OBJOUT= bin/
EXECOUT= ./
EXECNAME= main
INCLUDE= include/

ALL: bin/processlinks.o bin/parsefiles.o 
	$(CC) $(OBJOUT)* -o $(EXECOUT)$(EXECNAME)
bin/processlinks.o: src/processlinks.c src/parsefiles.c include/parsefiles.h
	$(CC) -c -I $(INCLUDE) src/processlinks.c -o $(OBJOUT)processlinks.o
bin/parsefiles.o: src/parsefiles.c include/parsefiles.h
	$(CC) -c -I $(INCLUDE) src/parsefiles.c -o $(OBJOUT)parsefiles.o
clean:
	-rm $(OBJOUT)* $(EXECOUT)$(EXECNAME) $(INCLUDE)*
run:
	mpiexec --hetero-apps -prefix /usr/local -hostfile machinefile ./main