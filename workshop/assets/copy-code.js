// Copy code functionality for workshop code blocks

function copyCode(button) {
    // Find the code block associated with this button
    const codeBlock = button.closest('.code-header').nextElementSibling.querySelector('code');
    
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

// Add copy buttons only to Terminal Command code blocks on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add copy buttons only to code blocks with "Terminal Command" header
    document.querySelectorAll('.code-header').forEach(header => {
        // Check if the header contains "Terminal Command" or "Terminal command"
        if (header.textContent.includes('Terminal') && !header.querySelector('.copy-button')) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-button';
            copyBtn.innerHTML = 'Copy';
            copyBtn.onclick = function() { copyCode(this); };
            header.appendChild(copyBtn);
        }
    });
});
