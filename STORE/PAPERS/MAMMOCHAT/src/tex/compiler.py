import subprocess
import re
from pathlib import Path
from typing import List, Optional


def extract_latex_error(output: str) -> Optional[str]:
    benign_warnings = [
        r".*float specifier changed to.*",
        r".*Overfull \\hbox.*",
        r".*Underfull \\hbox.*",
        r".*Package hyperref Warning.*",
        r".*LaTeX Warning: Label\(s\) may have changed.*",
        r".*pdfTeX warning.*destination with the same identifier.*",
        r".*duplicate ignored.*",
        r".*pdfTeX warning.*",
        r".*Package.*Warning.*",
        r".*LaTeX Warning.*",
        r".*Writer's Bureau.*",
        r".*Missing character.*",
        r".*Rerun to get.*",
        r".*has not changed.*",
        r".*Please.*run.*",
        r".*info.*warning.*",
        r".*checksum.*",
    ]
    
    error_patterns = [
        (r"!(.*?)(?=\n|$)", True),
        (r"(?s)!(.*?)(?=\n\n|\nl\.)", True),
        (r"LaTeX Error:(.*?)(?=\n|$)", False),
        (r"(?:Package|Class) (\w+) Error:(.*?)(?=\n|$)", False),
        (r"Missing(.*?)(?=\n|$)", False),
        (r"Undefined control sequence(.*?)(?=\n|$)", False),
        (r"No file (.*?)\.(.*?)(?=\n|$)", False),
        (r"Emergency stop\.", True),
        (r"!  ==> Fatal error occurred", True),
        (r"error:.*", True),
    ]
    
    lines = output.split('\n')
    filtered_lines = []
    
    for line in lines:
        is_benign = any(re.match(pattern, line, re.IGNORECASE) for pattern in benign_warnings)
        if not is_benign:
            filtered_lines.append(line)
    
    if not filtered_lines:
        return None
    
    filtered_output = '\n'.join(filtered_lines)
    
    errors = []
    for pattern, critical in error_patterns:
        matches = re.finditer(pattern, filtered_output, re.IGNORECASE)
        for m in matches:
            error = m.group(0).strip()
            if error:
                if critical:
                    return error
                errors.append(error)
    
    if errors:
        if "Output written on" in output and ".pdf" in output:
            success_indicators = [
                "Output written on",
                "PDF statistics:",
                "Here is how much of TeX's memory you used:",
            ]
            
            for indicator in success_indicators:
                if indicator in output:
                    return None
        
        return "\n".join(errors)
    
    return None


def run_tex_command(cmd: List[str], desc: str, cwd: Optional[Path] = None) -> bool:
    if subprocess.run(['which', cmd[0]], capture_output=True).returncode != 0:
        raise RuntimeError(f"{desc} failed: {cmd[0]} not found. Please ensure TeX Live is installed.")

    result = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=cwd
    )

    # Print stdout and stderr for debugging
    # if result.stdout:
    #     print("STDOUT:", result.stdout)
    # if result.stderr:
    #     print("STDERR:", result.stderr)

    error_msg = extract_latex_error(result.stdout)

    if error_msg or result.returncode != 0:
        if error_msg:
            full_error = f"{desc} failed with error:\n{error_msg}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            raise RuntimeError(full_error)
        else:
            full_error = f"{desc} failed with return code {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            raise RuntimeError(full_error)

    return True


def compile_latex_document(tex_file: str) -> bool:
    """Compile LaTeX document with full bibliography processing using latexmk"""

    tex_path = Path(tex_file)
    tex_dir = tex_path.parent
    tex_filename = tex_path.name

    # Use latexmk to handle the complete compilation process
    print("  Running latexmk compilation...")
    command = [
        "latexmk",
        "-pdf",
        "-bibtex",
        "-output-directory=.",
        tex_filename
    ]
    run_tex_command(command, "LaTeXmk compilation", cwd=tex_dir)

    return True