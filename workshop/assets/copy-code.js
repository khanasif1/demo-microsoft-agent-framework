// Copy code functionality for workshop code blocks

function copyCode(button) {
    // Find the code block associated with this button
    const codeBlock = button.closest('.code-header').nextElementSibling.querySelector('code') || 
                      button.closest('.code-block').querySelector('code');
    
    if (!codeBlock) return;
    
    const code = codeBlock.textContent;
    
    // Copy to clipboard
    navigator.clipboard.writeText(code).then(() => {
        // Update button state
        const originalText = button.innerHTML;
        button.classList.add('copied');
        button.innerHTML = 'Copied!';
        
        // Reset button after 2 seconds
        setTimeout(() => {
            button.classList.remove('copied');
            button.innerHTML = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy code:', err);
        button.innerHTML = 'Failed to copy';
        setTimeout(() => {
            button.innerHTML = originalText;
        }, 2000);
    });
}

// Add copy buttons to all code blocks on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add copy buttons to code blocks with headers
    document.querySelectorAll('.code-header').forEach(header => {
        if (!header.querySelector('.copy-button')) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-button';
            copyBtn.innerHTML = 'Copy';
            copyBtn.onclick = function() { copyCode(this); };
            header.appendChild(copyBtn);
        }
    });
    
    // Add copy buttons to standalone code blocks
    document.querySelectorAll('.code-block:not(.code-header + .code-block)').forEach(block => {
        if (!block.querySelector('.copy-button') && block.querySelector('code')) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-button';
            copyBtn.innerHTML = 'Copy';
            copyBtn.style.position = 'absolute';
            copyBtn.style.top = '10px';
            copyBtn.style.right = '10px';
            copyBtn.onclick = function() { copyCode(this); };
            block.style.position = 'relative';
            block.appendChild(copyBtn);
        }
    });
});
