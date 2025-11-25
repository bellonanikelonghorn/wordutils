import re
from docx import Document

def renumber_chapters(input_file, output_file):
    doc = Document(input_file)
    chapter_count = 1
    
    # Regex to find existing Chapter numbering (e.g., "Chapter 1", "Chapter One", "Chapter 5: Title")
    # This looks for "Chapter" at the start of the line, followed by space and any characters until a colon, dash, or end of line.
    pattern = re.compile(r'^(Chapter\s+\w+)(.*)', re.IGNORECASE)

    print(f"Processing {input_file}...")

    for paragraph in doc.paragraphs:
        # Check if the paragraph is styled as a Heading 1
        if paragraph.style.name.startswith('Heading 1'):
            text = paragraph.text.strip()
            
            # Check if the text actually starts with "Chapter"
            if text.lower().startswith("chapter"):
                # We split the line to preserve any Chapter Titles (e.g., "Chapter 5: The Fall")
                # If the chapter is just "Chapter 5", we replace it entirely.
                # If it is "Chapter 5: The Fall", we want "Chapter {new}: The Fall"
                
                # Simple split: Find the first separator like ':', '-', or just keep it simple
                if ':' in text:
                    title_part = text.split(':', 1)[1]
                    new_text = f"Chapter {chapter_count}:{title_part}"
                elif '–' in text: # En dash
                    title_part = text.split('–', 1)[1]
                    new_text = f"Chapter {chapter_count} –{title_part}"
                elif '-' in text: # Hyphen
                    title_part = text.split('-', 1)[1]
                    new_text = f"Chapter {chapter_count} -{title_part}"
                else:
                    # No title, just "Chapter X"
                    new_text = f"Chapter {chapter_count}"

                paragraph.text = new_text
                print(f"Renumbered: {new_text}")
                chapter_count += 1

    doc.save(output_file)
    print(f"Done! Saved as {output_file}")

# --- UPDATE THESE FILENAMES ---
input_filename = "YOUR FILE NAME HERE.docx" # The name of your combined file
output_filename = input_filename+ " Renumbered.docx" 

if __name__ == "__main__":
    try:
        renumber_chapters(input_filename, output_filename)
    except Exception as e:
        print(f"An error occurred: {e}")