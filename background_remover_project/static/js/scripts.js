const express = require('express');
const multer = require('multer');
const sharp = require('sharp'); // For image processing
const app = express();
const port = 3000;

// Middleware for file upload
const upload = multer({ dest: 'uploads/' });

app.post('/process-image', upload.single('image'), async (req, res) => {
    try {
        const file = req.file;

        if (!file) {
            return res.status(400).json({ success: false, message: 'No file uploaded' });
        }

        const originalPath = file.path;
        const processedPath = `processed-${file.filename}.png`;

        // Example: Remove background with Sharp
        await sharp(originalPath)
            .resize(800) // Optional: Resize
            .toFile(processedPath);

        res.json({
            success: true,
            original: `/uploads/${file.filename}`,
            processed: `/uploads/${processedPath}`,
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ success: false, message: 'Error processing image' });
    }
});

// Serve static files
app.use('/uploads', express.static('uploads'));

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
