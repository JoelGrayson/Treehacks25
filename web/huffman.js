huffman();

function huffman() {
    /** @type {HTMLCanvasElement} */
    const h = document.querySelector('#huffmanTree');
    h.width = 1200;
    h.height = 800;
    h.style.zoom=0.4;

    const ctx = h.getContext('2d');
    
    // Function to draw the tree
    function drawTree(node, x, y, xOffset, yOffset) {
        if (!node) return;
        
        ctx.beginPath();
        ctx.arc(x, y, 20, 0, 2 * Math.PI);
        ctx.fillStyle = node.char ? '#4CAF50' : '#2196F3';
        ctx.fill();
        ctx.stroke();
        
        ctx.fillStyle = 'white';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(node.char || node.code || '', x, y);
        
        if (node.left) {
            const newX = x - xOffset;
            const newY = y + yOffset;
            ctx.beginPath();
            ctx.moveTo(x, y + 20);
            ctx.lineTo(newX, newY - 20);
            ctx.stroke();
            drawTree(node.left, newX, newY, xOffset * 0.5, yOffset);
        }
        
        if (node.right) {
            const newX = x + xOffset;
            const newY = y + yOffset;
            ctx.beginPath();
            ctx.moveTo(x, y + 20);
            ctx.lineTo(newX, newY - 20);
            ctx.stroke();
            drawTree(node.right, newX, newY, xOffset * 0.5, yOffset);
        }
    }
    
    // Draw the tree
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, h.width, h.height);
    drawTree(huffmanTree.tree, h.width / 2, 50, 300, 100);
    
    console.log('Huffman tree visualization has been created.');
    
    // If running in a Node.js environment, we would save the canvas as an image
    // However, since we can't do that here, we'll just log the dimensions
    console.log(`Canvas dimensions: ${h.width}x${h.height}`);
}

