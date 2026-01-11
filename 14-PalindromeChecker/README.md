# Palindrome Checker

A Python program to check if words/phrases are palindrome

## HERE's THE CHEAT SHEET OF PALINDROME 
### To Check Any Text

def is_palindrome():
   cleaned = ''.join(char.lower() for char in text if char.isalum())
   return cleaned == cleaned[::-1]

## Quick Start

py main.py