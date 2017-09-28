/*
 * Gabrielle Boyce ~ CSC 222: Homework 4: Tech Shell
 * 2-17-2017
 * realtechshell.c
 * This code acts as a basic shell. It handles simple Linux commands and redirects. It handles piping. Will return errors if invalid Linux commands are used.
 * Piping assistance from https://www.quora.com/Unix-How-can-I-write-a-code-for-PIPE-in-C-shell-script-python
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include "HashTable2.h"

char str[128];
static char *ptr;
static char *arr[20]; // Token storage
static int j; //argument counter
static int scf = 0; // Flag for handling special characters
static char q = 0; // Assists in handling special characters during execution

void bufferTransfer(int srcFD, int destFD)
{
	//Uses a buffer to read from source by file descriptor and write the data to the destination by file descriptor.
	char buf[BUFSIZ]; //create character array the size of system buffer
	ssize_t bytes_read, bytes_written; //ssize_t is max amount of bytes that can be read/written at a time
	while ((bytes_read = read(srcFD, buf, BUFSIZ)) > 0) //read from source, store system buffer amount of bytes into buf
	{
		bytes_written = 0;
		while(bytes_written < bytes_read) //keep going until having written all the read bytes
		{
			bytes_written += write(destFD, buf + bytes_written, bytes_read - bytes_written);
			//write to destination file descriptor
			//write from buffer, starting at where you last left off if you haven't written it all yet
			//the size will by equal to all the bytes read, unless you haven't written it all yet
			//in which case, the size is what is remaining
		}
	}
	//by the end of this operation, srcFD has been read and written into destFD
}

int notbuilt(char *args[]){ // Not built-in command handler

	pid_t pid;
	pid = fork();
	// *argpt = args[0];
	int execstat;
	int g = 0;

	if(pid < 0){
		fprintf(stderr, "Fork failed");
		exit(-1);
	}

	else if (pid == 0)
	{
		//Check for special character tokens, do redirections if necessary
		for(q = 0; args[q] != '\0'; q++)
		{    //q = (g+1); // will be the special character
			if(args[q] ==  "<" || args[q] == ">" || args[q] == ">>")
			{ // Special token execution
				if(args[q] == ">"){ // > execution
					FILE *file;
					q++; // file name
					file = freopen(args[q], "w+", stdout);
					q--; // back to special char
					args[q] = '\0';
					execstat = execvp(args[0], args);
					if(execstat != 0){
						perror("Error:");
						_exit(0);
					}

					fclose(file);
					q--;

				}

				if(args[q] == "<"){ // < execution
					q++;
					freopen(args[q], "r", stdin);
					q--;
					args[q] = '\0';
					execstat = execvp(args[0], args);
					if(execstat != 0){
						perror("Error:");
						_exit(0);
					}


				}

				if(args[q] == ">>"){ // >> execution
					q++;

					freopen(args[q], "a", stdout);
					q--;
					args[q] = '\0';
					execstat = execvp(args[0], args);
					if(execstat != 0){
						perror("Error:");
						_exit(0);
					}
				}
				/** 
				  printf("Q is: %s\n", args[q]); //For later piping
				  printf("G before adding is: %s\n", args[g]);
				  g=g+2;
				  printf("G after adding is: %s\n", args[g]);
				  q--;
				 */
			}

			//piping
			if(args[q] == "|")
			{
				printf("Piping now\n");
				int status;
				//adjusted int pipeVar[2];
				//holding arguments for parent and child
				char* args1[8]; //first to execute, child
				char* args2[8]; //second to execute, parent
				for (int i = 0; i < 8; i++)
				{
					args1[i] =(char*) malloc(sizeof(char*));
					args2[i] =(char*) malloc(sizeof(char*));
				}
				printf("Args1 args: \n");
				for (int i = 0; i < q; i++)
				{
					strcpy(args1[i], args[i]);
					printf("%s ", args1[i]);
				}
				args1[q] = '\0'; printf("%s \n", args1[q]);
	
				printf("Args2 args: \n");
				for (int i = q + 1; i < j; i++)
				{
					strcpy(args2[i], args[i]);
					printf("%s ", args2[i]);
				}
				args2[j] = '\0'; printf("%s \n", args2[j]);
				
				int pipeVar[2]; //new
				pipe(pipeVar); //pipe creates two file decriptors: one for read, one for write end

				int pipe_pid1 = fork();
				if (pipe_pid1 < 0)
				{
					fprintf(stderr, "Fork failed");
					exit(-1);
				}
				else if (pipe_pid1 == 0) //child process
				{
					//child will execute first part of pipe
					//pipe[0] is read end, pipe[1] is write end
					//close read end of pipeVar
					close(pipeVar[0]);
					//remap output to pipe to parent
					dup2(pipeVar[1], 1);
					close(pipeVar[1]);
					//execute the process now that inputs and outputs have been arranged
					//printf("Executing child\n");
					//fflush(stdin);
					execstat = execvp(args1[0], args1);;
					if (execstat == -1)
					{
						perror("Pipe child execution failed");
						_exit(0);
					}
					//fflush(stdout);
					_exit(1);
				}
				int pipe_pid2 = fork();
				if (pipe_pid2 == 0) //parent process
				{
					//wait(NULL);
					close(pipeVar[1]);
					//read output from child, mapped as input
					dup2(pipeVar[0], 0);
					//close write  end of pipeVar
					close(pipeVar[0]);
					//read child's stdout

					//printf("Parent execution\n");
					//after all pipes completed, execute final argument
					execstat = execvp(args2[0], args2);
					if (execstat == -1)
					{
						perror ("Error");
						_exit(0);
					}
					//fflush(stdout);
					_exit(1);
				}
				close(pipeVar[0]);
				close(pipeVar[1]);
				while (wait(&status) != pipe_pid1);
				printf("A child has finished\n");
				_exit(0);
				break; //quit loop; we're done here after executing pipe
			}
		}
		//end of for loop checking for redirects
		//for(g=0; args[g] != '\0'; g++)
		//{
		printf("Executing normally\n");
		if(args[g] != "<" || args[g] != ">" || args[g] != ">>")
		{ 
			execstat = execvp(args[g], args);
			if(execstat == -1){
				perror("Error");}
		}
		_exit(1);
		//}

	}

	else{
		wait(NULL);
		//exit(0);
	}
}

int chd(char *args[]){ // CD - Change directory 
	char cwd[1024];
	if(chdir(args[1]) != 0){ 
		perror("\n chdir() error()");
	}
	else{
		if(getcwd(cwd, sizeof(cwd)) == NULL){
			perror("\n getcwd() error");
		}
		else{
			printf("\nAfter changing, current working directory is: %s\n", cwd);
		}
	}
}

int prwd(char *args[]){ // PWD - Print working directory
	char pwd[1024];
	if(getcwd(pwd, sizeof(pwd)) == NULL){
		perror("\ngetpwd() error");
	}
	else{
		printf("\nCurrent working directory is: %s\n", pwd);
	}
}

void checker(char *args[]){ //Built-in vs Not built-in detector

	//Built-in

	if(strcmp(args[0], "cd") == 0){ // cd command
		chd(args);
	}

	else if(strcmp(args[0], "pwd") == 0){ // pwd command
		prwd(args);

	}

	else if(strcmp(args[0], "exit") == 0){ // exit command
		exit(3);

	}

	else if(strcmp(args[0], "set") == 0){ // set command
		hashInsert(args[1], args[2]);

	}

	else if(strcmp(args[0], "list") == 0){ // list command
		hashDisplay();

	}

	//Not built-in

	else{
		notbuilt(args);
	}    
}



char *tokenizer(char* string) // Token parser 
{
	char *p;
	if(string != NULL) // Beginning of token & if content still to parse
	{
		ptr=string;
		p=string;
	}
	else
	{
		if(*ptr == '\0') // No content to parse
			return NULL;

		p=ptr;
	}

	while(*ptr != '\0')
	{
		//take care of quotation marks as a single token
		if(*ptr == '"')
		{
			ptr++;
			while(*ptr != '"')
			{
				ptr++; //get to the next quotation mark
			}
			ptr++; //get past quotation mark
			*ptr = '\0'; //End of token
			ptr++;
			return p; //Done with token, return the string
		}


		if(*ptr == ' ' || *ptr == '\t' || *ptr == '\v' || *ptr == '<' || *ptr == '>' || *ptr ==  '|') // Delimiters & special characters
		{
			if(ptr == p && (*ptr == ' ' || *ptr == '\t' || *ptr == '\v')) // Catch multiple spaces, tabs, vertical tabs
			{
				p++;

			} 
			else
			{
				if(*ptr == '|'){ // Flag | token
					scf = 1;
				}

				if(*ptr == '<'){ // Flag < token
					scf = 2;
				}

				if(*ptr == '>'){ // Flag >, >> token
					*ptr='\0';
					ptr++;
					scf = 3;
					if(*ptr == '>'){
						scf=4;
					}
					else{
						ptr--;
					}
				}

				*ptr='\0'; // End of token
				ptr++;
				return p;
			}
		}

		ptr++;
	}
	return p; // Beginning of token to null 
}

int main()
{
	int i;
	j=0;
	char *p_str, *token;
	int temp = 0;

	printf("\nEnter string to tokenize:  ");
	while(1)
	{
		j = 0;
		temp = 0;
		scanf(" %[^\n]", str);

		for(i=1, p_str = str; ; i++, p_str = NULL)
		{

			token = tokenizer(p_str);
			if(token == NULL)
				break;

			if(*token != '\0'){ // Print token & token number
				arr[j] = token;
				j++;
			}

			else{
				i--;
			}

			if(scf != 0){// Special character flags printed
				i++;
				if(scf == 1){
					arr[j] = "|";
				}
				if(scf==2){
					arr[j] = "<";
				}
				if(scf==3){
					arr[j] = ">";
				}
				if(scf==4){
					arr[j] = ">>";
				}
				j++;
				scf = 0;
			}
		}
		arr[j] = '\0'; //NULL
		//test and look at tokens
		//for(i = 0; i < j; i++)
			//printf("( %s )", arr[i]);

		checker(arr);
		printf("\n");
	}
}
