import os
import sys
import json
import re
from datetime import datetime
from collections import Counter
from typing import Dict, List, Tuple, Optional, Any


class TextAnalyzer:
    """Main text analyzer class with vowel counting and text analysis."""
    
    # Vowels in different languages
    VOWELS = {
        'english': {'a', 'e', 'i', 'o', 'u'},
        'english_y': {'a', 'e', 'i', 'o', 'u', 'y'},  # Sometimes Y
        'spanish': {'a', 'e', 'i', 'o', 'u'},
        'french': {'a', 'e', 'i', 'o', 'u', 'y', 'à', 'â', 'é', 'è', 'ê', 'ë', 'î', 'ï', 'ô', 'ö', 'ù', 'û', 'ü'},
        'german': {'a', 'e', 'i', 'o', 'u', 'ä', 'ö', 'ü'},
    }
    
    # Consonants
    CONSONANTS = set('bcdfghjklmnpqrstvwxyz')
    
    # Common words to ignore in analysis
    COMMON_WORDS = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
        'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
        'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me'
    }
    
    def __init__(self):
        """Initialize the text analyzer."""
        self.current_text = ""
        self.history = []
        self.analysis_cache = {}
        
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self) -> None:
        """Display the application banner."""
        banner = """
╔══════════════════════════════════════════════════════╗
║               🔤 TEXT ANALYZER 🔤                    ║
║        Count vowels & analyze text content!          ║
╚══════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "═" * 50)
        print("📋 MAIN MENU")
        print("═" * 50)
        print("1️  Input/Edit text")
        print("2️  Count vowels")
        print("3️  Full text analysis")
        print("4️  Find words with most vowels")
        print("5️  Vowel frequency analysis")
        print("6️  Compare texts")
        print("7️  Text statistics")
        print("8️  Palindrome checker")
        print("9️  Save/Load analysis")
        print("🔟  View history")
        print("0️ Exit")
        print("═" * 50)
    
    def get_menu_choice(self) -> str:
        """Get and validate menu choice."""
        while True:
            try:
                choice = input("\nEnter your choice (0-10): ").strip()
                if choice == '10' or choice in [str(i) for i in range(10)]:
                    return choice
                else:
                    print("❌ Please enter a number between 0 and 10")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
    
    def input_text(self) -> None:
        """Input or edit text."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📝 INPUT/EDIT TEXT")
        print("═" * 50)
        
        if self.current_text:
            print(f"\nCurrent text ({len(self.current_text)} characters):")
            self.display_text_preview(self.current_text)
            
            print("\nOptions:")
            print("1. Edit current text")
            print("2. Append new text")
            print("3. Clear text")
            print("4. Load sample text")
            print("5. Keep current text")
            
            option = input("\nChoose option (1-5): ").strip()
            
            if option == '2':
                print("\nEnter text to append (type 'done' on new line to finish):")
                new_text = self.get_multiline_input()
                self.current_text += "\n" + new_text if new_text else ""
                print(f"✅ Text appended. New length: {len(self.current_text)} characters")
                self.analysis_cache.clear()
                self.add_to_history("Appended text")
                return
            elif option == '3':
                self.current_text = ""
                print("✅ Text cleared")
                self.analysis_cache.clear()
                self.add_to_history("Cleared text")
                return
            elif option == '4':
                self.load_sample_text()
                return
            elif option == '5':
                return
        
        print("\nEnter your text (type 'done' on a new line to finish):")
        print("Type 'sample' to load sample text")
        print("Type 'cancel' to go back")
        
        text = self.get_multiline_input()
        
        if text is not None:
            self.current_text = text
            print(f"\n✅ Text saved! ({len(text)} characters)")
            self.analysis_cache.clear()
            self.add_to_history("Entered new text")
        else:
            print("❌ No text entered!")
        
        input("\nPress Enter to continue...")
    
    def get_multiline_input(self) -> Optional[str]:
        """Get multiline input from user."""
        lines = []
        print("\n" + "─" * 30)
        
        while True:
            try:
                line = input()
                
                if line.lower() == 'done':
                    break
                if line.lower() == 'cancel':
                    return None
                if line.lower() == 'sample':
                    return self.load_sample_text(return_text=True)
                
                lines.append(line)
                
            except KeyboardInterrupt:
                print("\n\n👋 Input cancelled.")
                return None
        
        return '\n'.join(lines)
    
    def load_sample_text(self, return_text: bool = False) -> Optional[str]:
        """Load sample text for demonstration."""
        samples = {
            '1': {
                'name': 'English Poem',
                'text': """Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date:"""
            },
            '2': {
                'name': 'Programming Quote',
                'text': """Any fool can write code that a computer can understand. 
Good programmers write code that humans can understand."""
            },
            '3': {
                'name': 'Science Fact',
                'text': """The quick brown fox jumps over the lazy dog. 
This sentence contains every letter in the English alphabet."""
            },
            '4': {
                'name': 'Long Sample',
                'text': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris."""
            }
        }
        
        print("\n📚 Sample Texts:")
        for key, sample in samples.items():
            print(f"{key}. {sample['name']} ({len(sample['text'])} chars)")
        
        choice = input("\nSelect sample (1-4) or Enter to cancel: ").strip()
        
        if choice in samples:
            sample = samples[choice]
            if return_text:
                return sample['text']
            
            self.current_text = sample['text']
            print(f"\n✅ Loaded '{sample['name']}'")
            print(f"Text length: {len(sample['text'])} characters")
            self.analysis_cache.clear()
            self.add_to_history(f"Loaded sample: {sample['name']}")
        else:
            print("❌ Invalid selection!")
        
        if not return_text:
            input("\nPress Enter to continue...")
        return None
    
    def display_text_preview(self, text: str, max_length: int = 200) -> None:
        """Display a preview of the text."""
        if not text:
            print("(Empty text)")
            return
        
        if len(text) <= max_length:
            print(f'"{text}"')
        else:
            preview = text[:max_length] + "..."
            print(f'"{preview}"')
        
        print(f"Length: {len(text)} characters, {len(text.split())} words")
    
    def count_vowels_basic(self, text: str, include_y: bool = False) -> Dict[str, int]:
        """
        Count vowels in text.
        
        Args:
            text: Text to analyze
            include_y: Whether to include 'y' as a vowel
            
        Returns:
            Dictionary with vowel counts
        """
        text_lower = text.lower()
        
        if include_y:
            vowels = self.VOWELS['english_y']
        else:
            vowels = self.VOWELS['english']
        
        counts = {vowel: 0 for vowel in vowels}
        
        for char in text_lower:
            if char in vowels:
                counts[char] += 1
        
        return counts
    
    def count_vowels_advanced(self, text: str) -> Dict[str, Any]:
        """
        Advanced vowel counting with various metrics.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with comprehensive vowel analysis
        """
        if not text:
            return {
                'total': 0,
                'vowel_counts': {},
                'percentage': 0,
                'vowel_density': 0,
                'most_common': None
            }
        
        # Basic counts
        counts = self.count_vowels_basic(text, include_y=False)
        counts_with_y = self.count_vowels_basic(text, include_y=True)
        
        # Calculate metrics
        total_chars = len(text)
        total_letters = sum(1 for c in text if c.isalpha())
        total_vowels = sum(counts.values())
        total_vowels_with_y = sum(counts_with_y.values())
        
        # Vowel percentage
        vowel_percentage = (total_vowels / total_letters * 100) if total_letters > 0 else 0
        vowel_percentage_with_y = (total_vowels_with_y / total_letters * 100) if total_letters > 0 else 0
        
        # Vowel density (vowels per word)
        words = text.split()
        vowel_density = total_vowels / len(words) if words else 0
        
        # Most common vowel
        most_common_vowel = max(counts.items(), key=lambda x: x[1]) if total_vowels > 0 else None
        
        # Vowel-consonant ratio
        consonants = sum(1 for c in text.lower() if c in self.CONSONANTS)
        vowel_consonant_ratio = total_vowels / consonants if consonants > 0 else 0
        
        return {
            'total': total_vowels,
            'total_with_y': total_vowels_with_y,
            'vowel_counts': counts,
            'vowel_counts_with_y': counts_with_y,
            'percentage': vowel_percentage,
            'percentage_with_y': vowel_percentage_with_y,
            'vowel_density': vowel_density,
            'most_common': most_common_vowel,
            'vowel_consonant_ratio': vowel_consonant_ratio,
            'total_letters': total_letters,
            'total_consonants': consonants
        }
    
    def run_vowel_count(self) -> None:
        """Run the vowel counting analysis."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔤 COUNT VOWELS")
        print("═" * 50)
        
        if not self.current_text:
            print("\n❌ No text to analyze!")
            print("Please input text first.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\nText preview ({len(self.current_text)} characters):")
        self.display_text_preview(self.current_text, 150)
        
        print("\nOptions:")
        print("1. Basic vowel count (a, e, i, o, u)")
        print("2. Include 'y' as vowel")
        print("3. Advanced analysis")
        
        try:
            option = int(input("\nChoose option (1-3): ").strip())
            
            if option == 1:
                self.display_basic_vowel_count()
            elif option == 2:
                self.display_vowel_count_with_y()
            elif option == 3:
                self.display_advanced_vowel_analysis()
            else:
                print("❌ Invalid option!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("\nPress Enter to continue...")
    
    def display_basic_vowel_count(self) -> None:
        """Display basic vowel count results."""
        counts = self.count_vowels_basic(self.current_text, include_y=False)
        total_vowels = sum(counts.values())
        
        print("\n" + "═" * 60)
        print("🔤 BASIC VOWEL COUNT")
        print("═" * 60)
        
        print(f"\nTotal vowels (a, e, i, o, u): {total_vowels}")
        
        if total_vowels > 0:
            print("\n" + "─" * 30)
            print("Vowel Distribution:")
            print("-" * 30)
            
            # Sort by count descending
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            
            for vowel, count in sorted_counts:
                percentage = (count / total_vowels * 100) if total_vowels > 0 else 0
                bar_length = int(percentage / 2)  # Scale to 50 chars max
                bar = "█" * bar_length
                print(f"{vowel.upper():2} : {count:4d} ({percentage:5.1f}%) {bar}")
        
        # Calculate percentage of letters that are vowels
        total_letters = sum(1 for c in self.current_text if c.isalpha())
        vowel_percentage = (total_vowels / total_letters * 100) if total_letters > 0 else 0
        
        print(f"\nVowels make up {vowel_percentage:.1f}% of all letters")
        
        self.add_to_history("Basic vowel count")
    
    def display_vowel_count_with_y(self) -> None:
        """Display vowel count including Y."""
        counts = self.count_vowels_basic(self.current_text, include_y=True)
        total_vowels = sum(counts.values())
        
        print("\n" + "═" * 60)
        print("🔤 VOWEL COUNT (INCLUDING Y)")
        print("═" * 60)
        
        print(f"\nTotal vowels (a, e, i, o, u, y): {total_vowels}")
        
        if total_vowels > 0:
            print("\n" + "─" * 30)
            print("Vowel Distribution:")
            print("-" * 30)
            
            # Sort by count descending
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            
            for vowel, count in sorted_counts:
                percentage = (count / total_vowels * 100) if total_vowels > 0 else 0
                bar_length = int(percentage / 2)
                bar = "█" * bar_length
                print(f"{vowel.upper():2} : {count:4d} ({percentage:5.1f}%) {bar}")
        
        # Comparison with basic count
        basic_counts = self.count_vowels_basic(self.current_text, include_y=False)
        basic_total = sum(basic_counts.values())
        y_count = counts.get('y', 0)
        
        print(f"\nComparison:")
        print(f"Vowels (without Y): {basic_total}")
        print(f"Y as vowel: {y_count}")
        print(f"Y contributes {y_count/total_vowels*100:.1f}% of total vowels")
        
        self.add_to_history("Vowel count with Y")
    
    def display_advanced_vowel_analysis(self) -> None:
        """Display advanced vowel analysis."""
        analysis = self.count_vowels_advanced(self.current_text)
        
        print("\n" + "═" * 60)
        print("📊 ADVANCED VOWEL ANALYSIS")
        print("═" * 60)
        
        print(f"\nText Statistics:")
        print(f"Total characters: {len(self.current_text)}")
        print(f"Total letters: {analysis['total_letters']}")
        print(f"Total consonants: {analysis['total_consonants']}")
        
        print(f"\n" + "─" * 30)
        print("Vowel Analysis:")
        print("-" * 30)
        
        print(f"Total vowels (a, e, i, o, u): {analysis['total']}")
        print(f"Total vowels (including Y): {analysis['total_with_y']}")
        print(f"Vowel percentage: {analysis['percentage']:.1f}%")
        print(f"Vowel percentage (with Y): {analysis['percentage_with_y']:.1f}%")
        print(f"Vowel density: {analysis['vowel_density']:.2f} vowels per word")
        print(f"Vowel-Consonant ratio: {analysis['vowel_consonant_ratio']:.2f}")
        
        if analysis['most_common']:
            vowel, count = analysis['most_common']
            print(f"Most common vowel: '{vowel}' ({count} occurrences)")
        
        # Detailed vowel distribution
        print(f"\n" + "─" * 30)
        print("Detailed Vowel Distribution:")
        print("-" * 30)
        
        for vowel, count in analysis['vowel_counts'].items():
            percentage = (count / analysis['total'] * 100) if analysis['total'] > 0 else 0
            print(f"{vowel.upper():2}: {count:4d} occurrences ({percentage:5.1f}%)")
        
        # Words analysis
        words = self.current_text.split()
        if words:
            print(f"\n" + "─" * 30)
            print("Word-level Analysis:")
            print("-" * 30)
            
            # Find words with most vowels
            word_vowel_counts = []
            for word in words:
                clean_word = ''.join(c for c in word if c.isalpha()).lower()
                if clean_word:
                    vowel_count = sum(1 for c in clean_word if c in self.VOWELS['english'])
                    word_vowel_counts.append((clean_word, vowel_count))
            
            # Top 5 words with most vowels
            word_vowel_counts.sort(key=lambda x: x[1], reverse=True)
            print("\nTop 5 words with most vowels:")
            for i, (word, count) in enumerate(word_vowel_counts[:5], 1):
                print(f"{i}. '{word}' - {count} vowels")
        
        self.add_to_history("Advanced vowel analysis")
    
    def run_full_analysis(self) -> None:
        """Run full text analysis."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📊 FULL TEXT ANALYSIS")
        print("═" * 50)
        
        if not self.current_text:
            print("\n❌ No text to analyze!")
            print("Please input text first.")
            input("\nPress Enter to continue...")
            return
        
        # Check cache first
        cache_key = f"full_analysis_{hash(self.current_text)}"
        if cache_key in self.analysis_cache:
            analysis = self.analysis_cache[cache_key]
        else:
            analysis = self.perform_full_analysis(self.current_text)
            self.analysis_cache[cache_key] = analysis
        
        self.display_full_analysis_results(analysis)
        input("\nPress Enter to continue...")
    
    def perform_full_analysis(self, text: str) -> Dict[str, Any]:
        """Perform comprehensive text analysis."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Character analysis
        total_chars = len(text)
        letters = sum(1 for c in text if c.isalpha())
        digits = sum(1 for c in text if c.isdigit())
        spaces = sum(1 for c in text if c.isspace())
        punctuation = sum(1 for c in text if not c.isalnum() and not c.isspace())
        
        # Word analysis
        total_words = len(words)
        unique_words = len(set(word.lower() for word in words))
        avg_word_length = sum(len(word) for word in words) / total_words if total_words > 0 else 0
        
        # Sentence analysis
        total_sentences = len(sentences)
        avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
        
        # Vowel analysis
        vowel_analysis = self.count_vowels_advanced(text)
        
        # Letter frequency
        letter_freq = Counter(c.lower() for c in text if c.isalpha())
        most_common_letters = letter_freq.most_common(5)
        
        # Word frequency
        word_freq = Counter(word.lower().strip('.,!?;:"\'') for word in words)
        most_common_words = word_freq.most_common(5)
        
        # Longest/shortest words
        if words:
            longest_word = max(words, key=len)
            shortest_word = min(words, key=len)
        else:
            longest_word = shortest_word = ""
        
        # Reading level approximation (Flesch Reading Ease simplified)
        syllables = self.estimate_syllables(text)
        reading_ease = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (syllables / total_words) if total_sentences > 0 and total_words > 0 else 0
        
        return {
            'basic': {
                'characters': total_chars,
                'letters': letters,
                'digits': digits,
                'spaces': spaces,
                'punctuation': punctuation,
                'words': total_words,
                'sentences': total_sentences,
                'unique_words': unique_words
            },
            'averages': {
                'word_length': avg_word_length,
                'sentence_length': avg_sentence_length,
                'syllables_per_word': syllables / total_words if total_words > 0 else 0
            },
            'vowel_analysis': vowel_analysis,
            'frequencies': {
                'letters': most_common_letters,
                'words': most_common_words
            },
            'extremes': {
                'longest_word': longest_word,
                'shortest_word': shortest_word
            },
            'readability': {
                'syllables': syllables,
                'reading_ease': reading_ease,
                'reading_level': self.get_reading_level(reading_ease)
            }
        }
    
    def estimate_syllables(self, text: str) -> int:
        """Estimate number of syllables in text (simplified)."""
        words = text.lower().split()
        total_syllables = 0
        
        for word in words:
            # Clean word
            word = ''.join(c for c in word if c.isalpha())
            if not word:
                continue
            
            # Simple syllable counting rules
            vowels = 'aeiouy'
            count = 0
            prev_char_vowel = False
            
            for char in word:
                if char in vowels:
                    if not prev_char_vowel:
                        count += 1
                    prev_char_vowel = True
                else:
                    prev_char_vowel = False
            
            # Adjustments
            if word.endswith('e'):
                count -= 1
            if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
                count += 1
            if count == 0:
                count = 1
            
            total_syllables += count
        
        return total_syllables
    
    def get_reading_level(self, reading_ease: float) -> str:
        """Convert Flesch Reading Ease to reading level."""
        if reading_ease >= 90:
            return "Very Easy (5th grade)"
        elif reading_ease >= 80:
            return "Easy (6th grade)"
        elif reading_ease >= 70:
            return "Fairly Easy (7th grade)"
        elif reading_ease >= 60:
            return "Standard (8th-9th grade)"
        elif reading_ease >= 50:
            return "Fairly Difficult (10th-12th grade)"
        elif reading_ease >= 30:
            return "Difficult (College)"
        else:
            return "Very Difficult (College Graduate)"
    
    def display_full_analysis_results(self, analysis: Dict[str, Any]) -> None:
        """Display full analysis results."""
        print(f"\nText preview ({len(self.current_text)} characters):")
        self.display_text_preview(self.current_text, 100)
        
        print("\n" + "═" * 60)
        print("📊 COMPREHENSIVE TEXT ANALYSIS")
        print("═" * 60)
        
        # Basic stats
        print(f"\n📈 BASIC STATISTICS:")
        print("-" * 40)
        basic = analysis['basic']
        print(f"Characters:     {basic['characters']:6d}")
        print(f"Letters:        {basic['letters']:6d} ({basic['letters']/basic['characters']*100:.1f}%)")
        print(f"Digits:         {basic['digits']:6d} ({basic['digits']/basic['characters']*100:.1f}%)")
        print(f"Spaces:         {basic['spaces']:6d} ({basic['spaces']/basic['characters']*100:.1f}%)")
        print(f"Punctuation:    {basic['punctuation']:6d} ({basic['punctuation']/basic['characters']*100:.1f}%)")
        print(f"Words:          {basic['words']:6d}")
        print(f"Sentences:      {basic['sentences']:6d}")
        print(f"Unique words:   {basic['unique_words']:6d} ({basic['unique_words']/basic['words']*100:.1f}%)")
        
        # Averages
        print(f"\n📐 AVERAGES:")
        print("-" * 40)
        averages = analysis['averages']
        print(f"Word length:    {averages['word_length']:.2f} characters")
        print(f"Sentence length: {averages['sentence_length']:.2f} words")
        print(f"Syllables/word: {averages['syllables_per_word']:.2f}")
        
        # Vowel analysis summary
        print(f"\n🔤 VOWEL SUMMARY:")
        print("-" * 40)
        vowel = analysis['vowel_analysis']
        print(f"Total vowels:   {vowel['total']:6d}")
        print(f"Vowel %:        {vowel['percentage']:6.1f}%")
        print(f"Most common:    {vowel['most_common'][0] if vowel['most_common'] else 'N/A'}")
        
        # Frequencies
        print(f"\n📊 FREQUENCIES:")
        print("-" * 40)
        print("Most common letters:")
        for letter, count in analysis['frequencies']['letters']:
            percentage = (count / analysis['basic']['letters'] * 100) if analysis['basic']['letters'] > 0 else 0
            print(f"  {letter.upper()}: {count:3d} ({percentage:.1f}%)")
        
        print("\nMost common words:")
        for word, count in analysis['frequencies']['words']:
            percentage = (count / analysis['basic']['words'] * 100) if analysis['basic']['words'] > 0 else 0
            print(f"  '{word}': {count:3d} ({percentage:.1f}%)")
        
        # Extremes
        print(f"\n🎯 EXTREMES:")
        print("-" * 40)
        extremes = analysis['extremes']
        if extremes['longest_word']:
            print(f"Longest word:   '{extremes['longest_word']}' ({len(extremes['longest_word'])} chars)")
            print(f"Shortest word:  '{extremes['shortest_word']}' ({len(extremes['shortest_word'])} chars)")
        
        # Readability
        print(f"\n📚 READABILITY:")
        print("-" * 40)
        readability = analysis['readability']
        print(f"Syllables:      {readability['syllables']:6d}")
        print(f"Reading ease:   {readability['reading_ease']:.1f}")
        print(f"Reading level:  {readability['reading_level']}")
        
        self.add_to_history("Full text analysis")
    
    def find_words_with_most_vowels(self) -> None:
        """Find and display words with most vowels."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔍 WORDS WITH MOST VOWELS")
        print("═" * 50)
        
        if not self.current_text:
            print("\n❌ No text to analyze!")
            print("Please input text first.")
            input("\nPress Enter to continue...")
            return
        
        words = self.current_text.split()
        if not words:
            print("\n❌ No words found in text!")
            input("\nPress Enter to continue...")
            return
        
        # Analyze each word
        word_analysis = []
        for word in words:
            clean_word = ''.join(c for c in word if c.isalpha()).lower()
            if clean_word:
                vowel_count = sum(1 for c in clean_word if c in self.VOWELS['english'])
                consonant_count = sum(1 for c in clean_word if c in self.CONSONANTS)
                total_letters = len(clean_word)
                vowel_percentage = (vowel_count / total_letters * 100) if total_letters > 0 else 0
                
                word_analysis.append({
                    'word': word,
                    'clean': clean_word,
                    'vowels': vowel_count,
                    'consonants': consonant_count,
                    'total': total_letters,
                    'percentage': vowel_percentage
                })
        
        # Sort by vowel count
        word_analysis.sort(key=lambda x: x['vowels'], reverse=True)
        
        print(f"\nAnalyzed {len(word_analysis)} words")
        print(f"Showing top 15 words by vowel count:\n")
        
        print("Rank  Word" + " " * 15 + "Vowels  Cons  Total  Vowel%")
        print("-" * 60)
        
        for i, analysis in enumerate(word_analysis[:15], 1):
            word_display = analysis['word'][:20] + "..." if len(analysis['word']) > 20 else analysis['word']
            print(f"{i:4d}  {word_display:20}  {analysis['vowels']:6d}  {analysis['consonants']:5d}  {analysis['total']:5d}  {analysis['percentage']:6.1f}%")
        
        # Summary statistics
        if word_analysis:
            avg_vowels = sum(w['vowels'] for w in word_analysis) / len(word_analysis)
            max_vowels = word_analysis[0]['vowels']
            min_vowels = word_analysis[-1]['vowels']
            
            print(f"\n📊 SUMMARY:")
            print(f"Average vowels per word: {avg_vowels:.2f}")
            print(f"Maximum vowels in a word: {max_vowels}")
            print(f"Minimum vowels in a word: {min_vowels}")
            
            # Find words with highest vowel percentage
            word_analysis.sort(key=lambda x: x['percentage'], reverse=True)
            print(f"\n🏆 Words with highest vowel percentage:")
            for i, analysis in enumerate(word_analysis[:5], 1):
                print(f"{i}. '{analysis['word']}' - {analysis['percentage']:.1f}% vowels")
        
        self.add_to_history("Found words with most vowels")
        input("\nPress Enter to continue...")
    
    def run_vowel_frequency_analysis(self) -> None:
        """Analyze vowel frequency patterns."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📈 VOWEL FREQUENCY ANALYSIS")
        print("═" * 50)
        
        if not self.current_text:
            print("\n❌ No text to analyze!")
            print("Please input text first.")
            input("\nPress Enter to continue...")
            return
        
        text_lower = self.current_text.lower()
        
        # Count vowel sequences
        vowel_sequences = []
        current_seq = ""
        
        for char in text_lower:
            if char in self.VOWELS['english']:
                current_seq += char
            elif current_seq:
                if len(current_seq) > 1:  # Only count sequences of 2+ vowels
                    vowel_sequences.append(current_seq)
                current_seq = ""
        
        if current_seq and len(current_seq) > 1:
            vowel_sequences.append(current_seq)
        
        # Analyze
        seq_counter = Counter(vowel_sequences)
        total_vowels = sum(1 for c in text_lower if c in self.VOWELS['english'])
        
        print(f"\nTotal vowels: {total_vowels}")
        print(f"Vowel sequences found: {len(vowel_sequences)}")
        
        if vowel_sequences:
            print(f"\n" + "─" * 40)
            print("VOWEL SEQUENCES (2+ vowels together):")
            print("-" * 40)
            
            for seq, count in seq_counter.most_common(10):
                percentage = (count / len(vowel_sequences) * 100)
                print(f"'{seq}': {count} times ({percentage:.1f}%)")
            
            # Most common vowel pairs
            print(f"\n" + "─" * 40)
            print("MOST COMMON VOWEL PAIRS:")
            print("-" * 40)
            
            vowel_pairs = Counter()
            for i in range(len(text_lower) - 1):
                pair = text_lower[i:i+2]
                if pair[0] in self.VOWELS['english'] and pair[1] in self.VOWELS['english']:
                    vowel_pairs[pair] += 1
            
            for pair, count in vowel_pairs.most_common(5):
                print(f"'{pair}': {count} times")
        
        # Vowel distribution by position in word
        print(f"\n" + "─" * 40)
        print("VOWEL POSITION IN WORDS:")
        print("-" * 40)
        
        words = self.current_text.split()
        position_counts = {'start': 0, 'middle': 0, 'end': 0}
        
        for word in words:
            clean_word = ''.join(c for c in word if c.isalpha()).lower()
            if clean_word:
                vowel_positions = [i for i, c in enumerate(clean_word) if c in self.VOWELS['english']]
                
                for pos in vowel_positions:
                    if pos == 0:
                        position_counts['start'] += 1
                    elif pos == len(clean_word) - 1:
                        position_counts['end'] += 1
                    else:
                        position_counts['middle'] += 1
        
        total_positions = sum(position_counts.values())
        if total_positions > 0:
            print("Vowel positions:")
            for position, count in position_counts.items():
                percentage = (count / total_positions * 100)
                print(f"  {position.title()}: {count} ({percentage:.1f}%)")
        
        self.add_to_history("Vowel frequency analysis")
        input("\nPress Enter to continue...")
    
    def compare_texts(self) -> None:
        """Compare vowel usage between two texts."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔄 COMPARE TEXTS")
        print("═" * 50)
        
        print("\nText 1 (Current text):")
        if self.current_text:
            self.display_text_preview(self.current_text, 100)
        else:
            print("(No current text)")
        
        print("\nEnter Text 2 for comparison:")
        print("Type 'done' on new line to finish, 'cancel' to go back")
        
        text2 = self.get_multiline_input()
        if text2 is None:
            print("❌ Comparison cancelled.")
            input("\nPress Enter to continue...")
            return
        
        if not text2:
            print("❌ No text entered for comparison!")
            input("\nPress Enter to continue...")
            return
        
        if not self.current_text:
            print("❌ No current text to compare with!")
            input("\nPress Enter to continue...")
            return
        
        # Analyze both texts
        analysis1 = self.count_vowels_advanced(self.current_text)
        analysis2 = self.count_vowels_advanced(text2)
        
        print("\n" + "═" * 60)
        print("📊 TEXT COMPARISON RESULTS")
        print("═" * 60)
        
        # Display comparison table
        print(f"\n{'Metric':<25} {'Text 1':<15} {'Text 2':<15} {'Difference':<15}")
        print("-" * 70)
        
        metrics = [
            ("Characters", len(self.current_text), len(text2)),
            ("Words", len(self.current_text.split()), len(text2.split())),
            ("Vowels", analysis1['total'], analysis2['total']),
            ("Vowel %", analysis1['percentage'], analysis2['percentage']),
            ("Vowels/Word", analysis1['vowel_density'], analysis2['vowel_density']),
        ]
        
        for name, val1, val2 in metrics:
            diff = val2 - val1
            diff_str = f"{diff:+.2f}" if isinstance(val1, float) else f"{diff:+d}"
            print(f"{name:<25} {val1:<15.2f if isinstance(val1, float) else val1} "
                  f"{val2:<15.2f if isinstance(val2, float) else val2} "
                  f"{diff_str:<15}")
        
        # Vowel distribution comparison
        print(f"\n" + "─" * 40)
        print("VOWEL DISTRIBUTION COMPARISON:")
        print("-" * 40)
        
        print(f"\n{'Vowel':<6} {'Text 1':<10} {'Text 2':<10} {'Diff':<10}")
        print("-" * 36)
        
        for vowel in 'aeiou':
            count1 = analysis1['vowel_counts'].get(vowel, 0)
            count2 = analysis2['vowel_counts'].get(vowel, 0)
            diff = count2 - count1
            print(f"{vowel.upper():<6} {count1:<10} {count2:<10} {diff:<+10}")
        
        # Determine which text is more vowel-rich
        if analysis1['percentage'] > analysis2['percentage']:
            print(f"\n🎯 Text 1 has more vowel density ({analysis1['percentage']:.1f}% vs {analysis2['percentage']:.1f}%)")
        elif analysis2['percentage'] > analysis1['percentage']:
            print(f"\n🎯 Text 2 has more vowel density ({analysis2['percentage']:.1f}% vs {analysis1['percentage']:.1f}%)")
        else:
            print(f"\n🎯 Both texts have equal vowel density ({analysis1['percentage']:.1f}%)")
        
        self.add_to_history("Compared texts")
        input("\nPress Enter to continue...")
    
    def run_text_statistics(self) -> None:
        """Display various text statistics."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📈 TEXT STATISTICS")
        print("═" * 50)
        
        if not self.current_text:
            print("\n❌ No text to analyze!")
            print("Please input text first.")
            input("\nPress Enter to continue...")
            return
        
        words = self.current_text.split()
        sentences = [s.strip() for s in re.split(r'[.!?]+', self.current_text) if s.strip()]
        
        print(f"\nText Statistics:")
        print(f"Characters: {len(self.current_text)}")
        print(f"Words: {len(words)}")
        print(f"Sentences: {len(sentences)}")
        print(f"Paragraphs: {self.current_text.count('\n\n') + 1}")
        
        # Word length distribution
        print(f"\n" + "─" * 40)
        print("WORD LENGTH DISTRIBUTION:")
        print("-" * 40)
        
        length_dist = Counter(len(word) for word in words)
        max_length = max(length_dist.keys()) if length_dist else 0
        
        for length in range(1, max_length + 1):
            count = length_dist.get(length, 0)
            if count > 0:
                percentage = (count / len(words)) * 100
                bar = "█" * int(percentage / 2)
                print(f"{length:2d} letters: {count:4d} ({percentage:5.1f}%) {bar}")
        
        # Sentence length distribution
        print(f"\n" + "─" * 40)
        print("SENTENCE LENGTH DISTRIBUTION:")
        print("-" * 40)
        
        sent_lengths = [len(sent.split()) for sent in sentences]
        if sent_lengths:
            sent_dist = Counter(sent_lengths)
            max_sent_length = max(sent_dist.keys())
            
            for length in sorted(sent_dist.keys()):
                count = sent_dist[length]
                percentage = (count / len(sentences)) * 100
                bar = "█" * int(percentage / 2)
                print(f"{length:2d} words:  {count:4d} ({percentage:5.1f}%) {bar}")
        
        # Character type breakdown
        print(f"\n" + "─" * 40)
        print("CHARACTER TYPE BREAKDOWN:")
        print("-" * 40)
        
        char_types = {
            'Letters': sum(1 for c in self.current_text if c.isalpha()),
            'Digits': sum(1 for c in self.current_text if c.isdigit()),
            'Spaces': sum(1 for c in self.current_text if c.isspace()),
            'Punctuation': sum(1 for c in self.current_text if not c.isalnum() and not c.isspace()),
            'Uppercase': sum(1 for c in self.current_text if c.isupper()),
            'Lowercase': sum(1 for c in self.current_text if c.islower()),
        }
        
        total_chars = len(self.current_text)
        for char_type, count in char_types.items():
            percentage = (count / total_chars) * 100
            bar = "█" * int(percentage / 2)
            print(f"{char_type:<12} {count:6d} ({percentage:5.1f}%) {bar}")
        
        self.add_to_history("Text statistics")
        input("\nPress Enter to continue...")
    
    def run_palindrome_checker(self) -> None:
        """Check for palindromes in text."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("🔄 PALINDROME CHECKER")
        print("═" * 50)
        
        if not self.current_text:
            print("\n❌ No text to analyze!")
            print("Please input text first.")
            input("\nPress Enter to continue...")
            return
        
        print("\nOptions:")
        print("1. Check if entire text is a palindrome")
        print("2. Find palindrome words in text")
        print("3. Find palindrome phrases")
        
        try:
            option = int(input("\nChoose option (1-3): ").strip())
            
            if option == 1:
                self.check_text_palindrome()
            elif option == 2:
                self.find_palindrome_words()
            elif option == 3:
                self.find_palindrome_phrases()
            else:
                print("❌ Invalid option!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("\nPress Enter to continue...")
    
    def is_palindrome(self, text: str) -> bool:
        """Check if text is a palindrome."""
        # Clean the text: remove non-alphanumeric, lowercase
        cleaned = ''.join(c.lower() for c in text if c.isalnum())
        return cleaned == cleaned[::-1]
    
    def check_text_palindrome(self) -> None:
        """Check if the entire text is a palindrome."""
        is_pal = self.is_palindrome(self.current_text)
        
        print(f"\nText: '{self.current_text[:50]}{'...' if len(self.current_text) > 50 else ''}'")
        print(f"Length: {len(self.current_text)} characters")
        
        if is_pal:
            print("\n✅ This text IS a palindrome!")
            
            # Show the palindrome structure
            cleaned = ''.join(c.lower() for c in self.current_text if c.isalnum())
            if len(cleaned) <= 30:
                print(f"\nPalindrome structure: {cleaned}")
                print(f"Reversed:             {cleaned[::-1]}")
        else:
            print("\n❌ This text is NOT a palindrome")
            
            # Find longest palindrome substring
            cleaned = ''.join(c.lower() for c in self.current_text if c.isalnum())
            longest_pal = self.find_longest_palindrome(cleaned)
            
            if longest_pal and len(longest_pal) > 1:
                print(f"\nLongest palindrome substring: '{longest_pal}' ({len(longest_pal)} chars)")
        
        self.add_to_history("Checked text palindrome")
    
    def find_longest_palindrome(self, text: str) -> str:
        """Find the longest palindrome substring."""
        if not text:
            return ""
        
        longest = ""
        n = len(text)
        
        # Check all substrings
        for i in range(n):
            for j in range(i, n):
                substring = text[i:j+1]
                if substring == substring[::-1] and len(substring) > len(longest):
                    longest = substring
        
        return longest
    
    def find_palindrome_words(self) -> None:
        """Find palindrome words in text."""
        words = self.current_text.split()
        palindrome_words = []
        
        for word in words:
            # Clean the word
            clean_word = ''.join(c.lower() for c in word if c.isalnum())
            if clean_word and self.is_palindrome(clean_word):
                palindrome_words.append((word, clean_word))
        
        print(f"\nFound {len(palindrome_words)} palindrome words:")
        
        if palindrome_words:
            print("\nWord (Original) -> Palindrome")
            print("-" * 50)
            
            for original, palindrome in palindrome_words:
                print(f"'{original}' -> '{palindrome}'")
            
            # Group by length
            print(f"\n📊 Palindrome words by length:")
            length_groups = {}
            for _, palindrome in palindrome_words:
                length = len(palindrome)
                if length not in length_groups:
                    length_groups[length] = 0
                length_groups[length] += 1
            
            for length in sorted(length_groups.keys()):
                count = length_groups[length]
                print(f"{length} letters: {count} word{'s' if count != 1 else ''}")
        
        self.add_to_history("Found palindrome words")
    
    def find_palindrome_phrases(self) -> None:
        """Find palindrome phrases (multiple words)."""
        # This is a simplified version - checks phrases up to 5 words
        words = self.current_text.split()
        found_phrases = []
        
        # Check phrases of different lengths
        for length in range(2, 6):  # 2 to 5 words
            for i in range(len(words) - length + 1):
                phrase = ' '.join(words[i:i+length])
                clean_phrase = ''.join(c.lower() for c in phrase if c.isalnum())
                
                if self.is_palindrome(clean_phrase):
                    found_phrases.append((phrase, clean_phrase))
        
        print(f"\nFound {len(found_phrases)} palindrome phrases:")
        
        if found_phrases:
            print("\nPhrase -> Cleaned Palindrome")
            print("-" * 60)
            
            for phrase, palindrome in found_phrases:
                print(f"'{phrase}'")
                print(f"  -> '{palindrome}' ({len(palindrome)} chars)")
                print()
        
        self.add_to_history("Found palindrome phrases")
    
    def save_load_analysis(self) -> None:
        """Save or load text analysis."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("💾 SAVE/LOAD ANALYSIS")
        print("═" * 50)
        
        print("\nOptions:")
        print("1. Save current text to file")
        print("2. Load text from file")
        print("3. Save analysis results")
        print("4. Load saved analysis")
        
        try:
            option = int(input("\nChoose option (1-4): ").strip())
            
            if option == 1:
                self.save_text_to_file()
            elif option == 2:
                self.load_text_from_file()
            elif option == 3:
                self.save_analysis_to_file()
            elif option == 4:
                self.load_analysis_from_file()
            else:
                print("❌ Invalid option!")
        
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("\nPress Enter to continue...")
    
    def save_text_to_file(self) -> None:
        """Save current text to a file."""
        if not self.current_text:
            print("❌ No text to save!")
            return
        
        filename = input("\nEnter filename (default: text.txt): ").strip()
        if not filename:
            filename = "text.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.current_text)
            
            print(f"✅ Text saved to '{filename}'")
            print(f"Characters saved: {len(self.current_text)}")
            self.add_to_history(f"Saved text to {filename}")
        
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    
    def load_text_from_file(self) -> None:
        """Load text from a file."""
        filename = input("\nEnter filename to load: ").strip()
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()
            
            self.current_text = text
            print(f"✅ Text loaded from '{filename}'")
            print(f"Characters loaded: {len(text)}")
            self.analysis_cache.clear()
            self.add_to_history(f"Loaded text from {filename}")
        
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found!")
        except Exception as e:
            print(f"❌ Error loading file: {e}")
    
    def save_analysis_to_file(self) -> None:
        """Save analysis results to a JSON file."""
        if not self.current_text:
            print("❌ No text to analyze!")
            return
        
        analysis = self.perform_full_analysis(self.current_text)
        
        filename = input("\nEnter filename (default: analysis.json): ").strip()
        if not filename:
            filename = "analysis.json"
        
        try:
            # Add metadata
            analysis['metadata'] = {
                'analyzed_at': datetime.now().isoformat(),
                'text_length': len(self.current_text),
                'text_preview': self.current_text[:100] + ("..." if len(self.current_text) > 100 else "")
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Analysis saved to '{filename}'")
            self.add_to_history(f"Saved analysis to {filename}")
        
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
    
    def load_analysis_from_file(self) -> None:
        """Load analysis results from a JSON file."""
        filename = input("\nEnter filename to load: ").strip()
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
            
            print(f"\n✅ Analysis loaded from '{filename}'")
            
            if 'metadata' in analysis:
                meta = analysis['metadata']
                print(f"Analyzed: {meta.get('analyzed_at', 'Unknown')}")
                print(f"Text preview: {meta.get('text_preview', 'N/A')}")
            
            # Display summary
            if 'basic' in analysis:
                basic = analysis['basic']
                print(f"\nSummary:")
                print(f"Characters: {basic.get('characters', 'N/A')}")
                print(f"Words: {basic.get('words', 'N/A')}")
                print(f"Vowels: {analysis.get('vowel_analysis', {}).get('total', 'N/A')}")
        
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found!")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON file!")
        except Exception as e:
            print(f"❌ Error loading analysis: {e}")
    
    def view_history(self) -> None:
        """View operation history."""
        self.clear_screen()
        print("\n" + "═" * 50)
        print("📜 OPERATION HISTORY")
        print("═" * 50)
        
        if not self.history:
            print("\nNo history yet!")
            print("Perform operations to see history here.")
        else:
            print(f"\nTotal operations: {len(self.history)}")
            print("\n" + "─" * 40)
            
            for i, entry in enumerate(reversed(self.history[-20:]), 1):
                timestamp = entry.get('timestamp', 'Unknown')
                action = entry.get('action', 'Unknown')
                print(f"{i:2d}. {timestamp} - {action}")
        
        print("\n" + "═" * 50)
        input("\nPress Enter to continue...")
    
    def add_to_history(self, action: str) -> None:
        """Add an action to history."""
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'action': action
        }
        self.history.append(entry)
        
        # Keep only last 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def run(self) -> None:
        """Main application loop."""
        while True:
            self.clear_screen()
            self.display_banner()
            
            # Show current text info
            if self.current_text:
                print(f"\n📝 Current text: {len(self.current_text)} characters, {len(self.current_text.split())} words")
                self.display_text_preview(self.current_text, 80)
            else:
                print("\n📝 No text loaded. Enter text to begin analysis!")
            
            self.display_menu()
            
            choice = self.get_menu_choice()
            
            if choice == '0':  # Exit
                print("\n👋 Thank you for using Text Analyzer!")
                print("Happy analyzing! 🔤")
                break
            
            elif choice == '1':  # Input/Edit text
                self.input_text()
            
            elif choice == '2':  # Count vowels
                self.run_vowel_count()
            
            elif choice == '3':  # Full analysis
                self.run_full_analysis()
            
            elif choice == '4':  # Words with most vowels
                self.find_words_with_most_vowels()
            
            elif choice == '5':  # Vowel frequency
                self.run_vowel_frequency_analysis()
            
            elif choice == '6':  # Compare texts
                self.compare_texts()
            
            elif choice == '7':  # Text statistics
                self.run_text_statistics()
            
            elif choice == '8':  # Palindrome checker
                self.run_palindrome_checker()
            
            elif choice == '9':  # Save/Load
                self.save_load_analysis()
            
            elif choice == '10':  # View history
                self.view_history()


def main():
    """Main function to run the text analyzer."""
    try:
        analyzer = TextAnalyzer()
        analyzer.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy analyzing!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please try running the application again.")


if __name__ == "__main__":
    main()