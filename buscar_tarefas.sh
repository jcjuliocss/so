#!/bin/bash
while IFS='-' read -r linha || [[ -n "$linha" ]]; do
	echo "$linha"
done < "tarefas.txt"
