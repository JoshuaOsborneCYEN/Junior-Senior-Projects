#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <iostream>
#include "HashTable.h"

main()
{
	HashTable table;
	const char s[2] = " ";
	char *token;

	char *newKey;
	char *newData;
	table.display();
	while(1)
	{
		char input[100];
		scanf(" %[^\n]", input);
		token = strtok(input, s);
		//First input is key
		newKey = token;
		token = strtok(NULL, s);
		//Second input is data
		newData = token;
		
		table.insert(newKey, newData);
		table.display();
		token = NULL;
		newKey = NULL;
		newData = NULL;
	}
	return 0;
}
