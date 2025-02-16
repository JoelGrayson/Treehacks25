huffman();

function huffman() {
    /** @type {HTMLCanvasElement} */

    // Create a canvas element
      const canvas = document.getElementById('huffmanTree');
      canvas.width = 1100;  // Increased width for better spacing
    canvas.height = 800;  // Increased height for better spacing
        // document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');

        // Function to draw a node
        function drawNode(x, y, label, isLeaf, char = '') {
        const radius = 20;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, 2 * Math.PI);
        // ctx.fillStyle = isLeaf ? '#4CAF50' : '#2196F3';
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = 'white';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        if (isLeaf) {
            ctx.fillText(char, x, y - 6);
            ctx.fillText(label, x, y + 6);
        } else {
            ctx.fillText(label, x, y);
        }
        }

        // Function to draw a line
        function drawLine(x1, y1, x2, y2) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
        }

        // Clear canvas
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Draw nodes - hardcoded positions with more spacing
        drawNode(500, 50, '', false);  // Root

        // Level 1
        drawNode(250, 120, '0', false);
        drawNode(750, 120, '1', false);

        // Level 2
        drawNode(125, 190, '00', false);
        drawNode(375, 190, '01', false);
        drawNode(625, 190, '10', false);
        drawNode(875, 190, '11', false);

        // Level 3
        drawNode(62, 260, '000', false);
        drawNode(187, 260, '001', true, 'e');
        drawNode(312, 260, '010', false);
        drawNode(437, 260, '011', true, ' ');
        drawNode(562, 260, '100', false);
        drawNode(687, 260, '101', false);
        drawNode(812, 260, '110', false);
        drawNode(937, 260, '111', false);

        // Level 4
        drawNode(31, 330, '0000', false);
        drawNode(93, 330, '0001', false);
        drawNode(281, 330, '0100', true, 'r');
        drawNode(343, 330, '0101', true, 's');
        drawNode(531, 330, '1000', false);
        drawNode(593, 330, '1001', true, 'n');
        drawNode(656, 330, '1010', true, 'o');
        drawNode(718, 330, '1011', true, 'i');
        drawNode(781, 330, '1100', true, 'a');
        drawNode(843, 330, '1101', false);
        drawNode(906, 330, '1110', true, 't');
        drawNode(968, 330, '1111', false);

        // Level 5
        drawNode(15, 400, '00000', true, 'm');
        drawNode(46, 400, '00001', true, 'u');
        drawNode(77, 400, '00010', false);
        drawNode(108, 400, '00011', false);
        drawNode(515, 400, '10000', true, 'c');
        drawNode(546, 400, '10001', true, 'd');
        drawNode(827, 400, '11010', false);
        drawNode(858, 400, '11011', true, 'l');
        drawNode(952, 400, '11110', false);
        drawNode(983, 400, '11111', true, 'h');

        // Level 6
        drawNode(62, 470, '000100', true, '>');
        drawNode(93, 470, '000101', true, 'b');
        drawNode(124, 470, '000110', true, 'y');
        drawNode(155, 470, '000111', true, 'w');
        drawNode(811, 470, '110100', true, 'g');
        drawNode(842, 470, '110101', true, 'p');
        drawNode(937, 470, '111100', false);

        // Level 7
        drawNode(921, 540, '1111000', true, 'v');
        drawNode(952, 540, '1111001', false);

        // Level 8
        drawNode(937, 610, '11110010', true, 'k');
        drawNode(968, 610, '11110011', false);

        // Level 9
        drawNode(952, 680, '111100110', true, 'x');
        drawNode(983, 680, '111100111', false);

        // Level 10
        drawNode(968, 750, '1111001110', true, 'j');
        drawNode(999, 750, '1111001111', false);

        // Level 11
        drawNode(984, 780, '11110011110', true, 'z');
        drawNode(1015, 780, '11110011111', true, 'q');


        // Draw lines
        drawLine(500, 65, 250, 105);   // Root to Level 1 left
        drawLine(500, 65, 750, 105);   // Root to Level 1 right

        // Level 1 to Level 2
        drawLine(250, 135, 125, 175);
        drawLine(250, 135, 375, 175);
        drawLine(750, 135, 625, 175);
        drawLine(750, 135, 875, 175);

        // Level 2 to Level 3
        drawLine(125, 205, 62, 245);
        drawLine(125, 205, 187, 245);
        drawLine(375, 205, 312, 245);
        drawLine(375, 205, 437, 245);
        drawLine(625, 205, 562, 245);
        drawLine(625, 205, 687, 245);
        drawLine(875, 205, 812, 245);
        drawLine(875, 205, 937, 245);

        // Level 3 to Level 4
        drawLine(62, 275, 31, 315);
        drawLine(62, 275, 93, 315);
        drawLine(312, 275, 281, 315);
        drawLine(312, 275, 343, 315);
        drawLine(562, 275, 531, 315);
        drawLine(562, 275, 593, 315);
        drawLine(687, 275, 656, 315);
        drawLine(687, 275, 718, 315);
        drawLine(812, 275, 781, 315);
        drawLine(812, 275, 843, 315);
        drawLine(937, 275, 906, 315);
        drawLine(937, 275, 968, 315);

        // Level 4 to Level 5
        drawLine(31, 345, 15, 385);
        drawLine(31, 345, 46, 385);
        drawLine(93, 345, 77, 385);
        drawLine(93, 345, 108, 385);
        drawLine(531, 345, 515, 385);
        drawLine(531, 345, 546, 385);
        drawLine(843, 345, 827, 385);
        drawLine(843, 345, 858, 385);
        drawLine(968, 345, 952, 385);
        drawLine(968, 345, 983, 385);

        // Level 5 to Level 6
        drawLine(77, 415, 62, 455);
        drawLine(77, 415, 93, 455);
        drawLine(108, 415, 124, 455);
        drawLine(108, 415, 155, 455);
        drawLine(827, 415, 811, 455);
        drawLine(827, 415, 842, 455);
        drawLine(952, 415, 937, 455);

        // Level 6 to Level 7
        drawLine(937, 485, 921, 525);
        drawLine(937, 485, 952, 525);

        // Level 7 to Level 8
        drawLine(952, 555, 937, 595);
        drawLine(952, 555, 968, 595);

        // Level 8 to Level 9
        drawLine(968, 625, 952, 665);
        drawLine(968, 625, 983, 665);

        // Level 9 to Level 10
        drawLine(983, 695, 968, 735);
        drawLine(983, 695, 999, 735);

        // Level 10 to Level 11
        drawLine(999, 765, 984, 775);
        drawLine(999, 765, 1015, 775);


        // Add title
        // ctx.fillStyle = 'black';
        // ctx.font = 'bold 20px Arial';
        // ctx.textAlign = 'center';
        // ctx.fillText('Huffman Tree Visualization', canvas.width / 2, 25);

        console.log('Improved Huffman tree visualization has been created.');
        console.log(`Canvas dimensions: ${canvas.width}x${canvas.height}`);
}

