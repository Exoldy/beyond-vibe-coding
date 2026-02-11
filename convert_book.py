import os
import re
import glob

def process_text(content):
    # Detect Figure lines and convert to placeholder
    # Example: Figure 1-1. Description...
    # We want to catch the whole paragraph if it starts with Figure/fig
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        s_line = line.strip()
        
        # Figure Detection
        if re.match(r'^Figure \d+[-.]\d+', s_line):
            # It's a figure caption
            new_lines.append(f"\n> [!NOTE]\n> **Image Missing**\n> *{s_line}*\n")
            continue

        # Subheader Detection Heuristic
        # - Not a Chapter header (handled at split level)
        # - Start with Uppercase
        # - No ending punctuation (., ?, !)
        # - Short length (< 100 chars)
        # - Not empty
        if (s_line and s_line[0].isupper() 
            and not s_line.endswith('.') 
            and not s_line.endswith(':') # Colons might be headers, but often lead-ins. Let's assume headers don't have colons for now, or do? "Introduction: What Is..." is a header.
            and len(s_line) < 100 
            and not s_line.startswith('>')
            and not re.match(r'^Step \d+', s_line) # avoid some artifacts
            ):
             # Check if it looks distinct (e.g. not just a sentence fragment)
             # Let's try to be conservative. If it has no punctuation at all.
             if not re.search(r'[.,;!?]', s_line):
                 new_lines.append(f"## {s_line}")
                 continue
                 
        new_lines.append(line)
            
    return '\n'.join(new_lines)


def main():
    output_dir = "book_md"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all txt files, exclude common junk
    files = sorted(glob.glob("*.txt"))
    
    toc_entries = []
    
    print(f"Found files: {files}")

    for filename in files:
        if filename == "requirements.txt" or filename == "convert_book.py":
            continue
            
        print(f"Processing {filename}...")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Fallback for weird encodings if any
            with open(filename, 'r', encoding='latin-1') as f:
                content = f.read()

        # Split by "Chapter X."
        # Use regex capture group to keep the delimiter (the chapter title line)
        parts = re.split(r'(^Chapter \d+\..*)', content, flags=re.MULTILINE)
        
        # parts[0] is text before first chapter.
        # parts[1] is Chapter Header, parts[2] is body, etc.
        
        sections = []
        
        if len(parts) > 1:
            # Handle preamble if significant
            if parts[0].strip():
                 # Heuristic: if file is "1 - Part I...", preamble usually contains "Part I..."
                 # We can save it as a separate file or prepend to first chapter.
                 # Let's clean it up and make it a section "Introduction" or similar if it's long.
                 # For "Part I", the first line is the Part title usually?
                 preamble_lines = parts[0].strip().split('\n')
                 header = preamble_lines[0] if preamble_lines else "Introduction"
                 sections.append((header, parts[0]))

            for i in range(1, len(parts), 2):
                header = parts[i].strip()
                body = parts[i+1] if i+1 < len(parts) else ""
                sections.append((header, body))
        else:
            # Entire file is one section
            # Check if filename has a number like "0 - Preface"
            base = os.path.splitext(filename)[0]
            # remove leading numbers for title
            header = re.sub(r'^\d+\s*-\s*', '', base)
            sections.append((header, content))

        for header, body in sections:
            processed_body = process_text(body)
            
            # Sanitize filename
            # e.g. "Chapter 1. Introduction: What Is..." -> "Chapter_1_Introduction"
            safe_name = re.sub(r'[^\w\s-]', '', header)
            safe_name = re.sub(r'\s+', '_', safe_name)
            if len(safe_name) > 50:
                 safe_name = safe_name[:50]
            
            # Ensure unique filenames
            out_path = os.path.join(output_dir, f"{safe_name}.md")
            counter = 1
            while os.path.exists(out_path):
                 out_path = os.path.join(output_dir, f"{safe_name}_{counter}.md")
                 counter += 1
            
            final_content = f"# {header}\n\n{processed_body}"
            
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
                
            # Add to TOC
            rel_path = os.path.basename(out_path)
            toc_entries.append(f"- [{header}]({rel_path})")

    # Write README
    with open(os.path.join(output_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write("# Book Content\n\n")
        f.write("\n".join(toc_entries))
        
    print("Conversion complete.")

if __name__ == "__main__":
    main()
