/**Created using help from https://www.tutorialspoint.com/data_structures_algorithms/hash_table_program_in_c.htm
 * Joshua Osborne
 * 4/12/2017
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <iostream>

#define SIZE 30

using namespace std;

/*
 * This struct defines the basic building blocks for the hash table
 */
typedef struct
{
	char *data;
	char *key;
} DataItem;

class HashTable
{
public:
	unsigned long hashCode(char* str);
	void insert(char* key, char* data);
	DataItem* search(char* key);
	DataItem* remove(char* key);
	void display();
private:
	DataItem* hashArray[SIZE];
	DataItem* item;
	DataItem* dummyItem;
};

//DataItem* hashArray[SIZE];
//DataItem* dummyItem;
//DataItem* item;

/**
  * This method generates a hash from a string
  */
unsigned long HashTable::hashCode(char *str)
{
	unsigned long hash = 5381;
	int c;

	while (c = *str++)
		hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

	return hash % SIZE;
}

void HashTable::insert(char *key, char *data)
{
	//allocate space in memory for new DataItem
	DataItem* item = (DataItem*) malloc(sizeof(DataItem));
	//allocate memory for new strings
	char* newData = (char*) malloc(sizeof(char) * 30);
	char* newKey = (char*) malloc(sizeof(char) * 30);
	//copy input into allocated memory
	strcpy(newData, data);
	strcpy(newKey, key);
	//add new allocated memory to the storage item
	item->data = newData;
	item->key = newKey;

	//get the hash
	int hashIndex = hashCode(key);
	printf("%d hashindex\n", hashIndex);
	//move in array until reaching an empty or deleted cell
	while(hashArray[hashIndex] != NULL) //&& hashArray[hashIndex]->key != NULL)
	{
		//go to next cell
		++hashIndex;
		//wrap around table if necessary
		hashIndex %= SIZE;
	}

	//insert item into hash table
	hashArray[hashIndex] = item;
}

DataItem* HashTable::search(char *key)
{
	//get the hash
	int hashIndex = hashCode(key);

	//move in array until finding empty spot
	while(hashArray[hashIndex] != NULL)
	{
		//look for matching key
		if(strcmp(hashArray[hashIndex]->key, key) != 0)
			return hashArray[hashIndex];

		//go to next cell
		++hashIndex;
		//wrap around table if necessary
		hashIndex %= SIZE;
	}
	//Not found
	return NULL;
}

DataItem* HashTable::remove(char *key)
{
	//get the hash
	int hashIndex = hashCode(key);
	//move in array until finding empty spot
	while(hashArray[hashIndex] != NULL)
	{
		if(strcmp(hashArray[hashIndex]->key, key) != 0)
		{
			DataItem* temp = hashArray[hashIndex];

			//assign a dummy item at deleted position
			hashArray[hashIndex] = dummyItem;

			return temp;
		}

		//go to next cell
		++hashIndex;
		//wrap around table if necessary
		hashIndex %= SIZE;
	}
}

void HashTable::display()
{
	//Prints all the key-value pairs in the array
	for(int i = 0; i < SIZE; i++)
	{
		if(hashArray[i] != NULL)
		{
			printf("%d displaying \n", i);
			printf("%d, %d)\n", hashArray[i]->key, hashArray[i]->data);
			printf(" (%s, %s) ", hashArray[i]->key, hashArray[i]->data);
		}
	}

	printf("\n");

}
/**
int main()
{
	const char s[2] = " ";
	char *token;

	char *newKey;
	char *newData;
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
		
		insert(newKey, newData);
		display();
		token = NULL;
		newKey = NULL;
		newData = NULL;
	}
	return 0;
}
*/
