require('dotenv').config();
const express = require('express'); // Moved this line to the top
const cors = require('cors');
const path = require('path');
const getGenAIResponse = require('./api/genai'); // Import GenAI API call function

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

// Test GenAI integration
app.get('/api/test-genai', async (req, res) => {
    try {
        const response = await getGenAIResponse("Hello, GenAI!");
        res.send(response);
    } catch (error) {
        res.status(500).send("Error in GenAI response.");
    }
});

// Route for main pages
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/signup', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'signup.html'));
});

app.get('/dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

// Other routes
const pages = [
    'aptitude', 'aptitudecontent', 'aptitudenext', 'grammar', 'grammarcontent', 
    'grammarnext', 'results', 'technical', 'technicalcontent', 'technicalnext', 
    'test', 'vocabcontent', 'vocabnext', 'speech', 'speechcontent', 'speechnext'
];

pages.forEach(page => {
    app.get(`/${page}`, (req, res) => {
        res.sendFile(path.join(__dirname, 'public', `${page}.html`));
    });
});



// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});



const { getChatbotResponse } = require('./chatbot');  // Function to get AI response

app.use(express.json());

app.post('/api/chat', async (req, res) => {
    const { message } = req.body;
    try {
        const reply = await getChatbotResponse(message);  // Call to AI model function
        res.json({ reply });
    } catch (error) {
        res.status(500).json({ error: 'Error generating response' });
    }
});

// Your existing code to start server...