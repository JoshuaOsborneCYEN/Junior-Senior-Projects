/*
 * Gabrielle Boyce ~ CSC 222: Homework 4: Tech Shell
 * 2-17-2017
 * realtechshell.c
 * This code acts as a basic shell. It handles simple Linux commands and redirects. It does not handle piping. Will return errors if invalid Linux commands are used.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

char str[128];
static char *ptr;
static char *arr[20]; // Token storage
static int j;
static int scf = 0; // Flag for handling special characters
static char q = 0; // Assists in handling special characters during execution

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
    
    else if (pid == 0){
      for(g=0; args[g] != '\0'; g++){
	q = (g+1); // will be the special character
	if(args[q] ==  "<" || args[q] == ">" || args[q] == ">>"){ // Special token execution
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
       
	else if(args[g] != "<" || args[g] != ">" || args[g] != ">>"){ 
	    execstat = execvp(args[g], args);
	    if(execstat == -1){
	      perror("Error");}
	}
	
      }
       
    
      
    }
    
      else{
	wait(NULL);
	exit(0);
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
  scanf("%[^\n]", str);

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
   checker(arr);
  printf("\n");
}
