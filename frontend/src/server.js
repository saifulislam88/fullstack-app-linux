import express from 'express';
import session from 'express-session';
import multer from 'multer';
import FormData from 'form-data';
import axios from 'axios';
import path from 'path';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';

dotenv.config();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const API_BASE = process.env.BACKEND_API_BASE_URL || 'http://127.0.0.1:8000';
const PORT = process.env.PORT || 3000;

const app = express();
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.urlencoded({ extended: true }));
app.use(session({ secret: process.env.SESSION_SECRET || 'dev-secret', resave: false, saveUninitialized: false }));

const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 2 * 1024 * 1024 } }); // 2MB

// GET form
app.get('/student/register', (req, res) => {
  res.render('student_register', { error: null });
});

// POST form + forward to backend
app.post('/student/register', upload.single('photo'), async (req, res) => {
  console.log('Frontend received /student/register POST, file:', req.file ? req.file.originalname : 'no file');
  try {
    if (!req.file) {
      return res.status(400).render('student_register', { error: 'No photo file uploaded' });
    }
    const fd = new FormData();
    const fields = ['name','institute','batch','course_name','module','email','password'];
    for (const f of fields) {
      fd.append(f, req.body[f] || '');
    }
    fd.append('photo', req.file.buffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype
    });
    const headers = fd.getHeaders();
    const resp = await axios.post(`${API_BASE}/api/students/register`, fd, { headers });
    console.log('Backend response:', resp.status, resp.data);
    res.redirect('/student/login');
  } catch (err) {
    console.error('Error forwarding to backend:', err.response?.data || err.message);
    const msg = err.response?.data?.detail || 'Registration failed';
    res.status(400).render('student_register', { error: msg });
  }
});

app.get('/student/login', (req, res) => res.send('Login page – after registration'));

// Start server
app.listen(PORT, () => console.log(`Frontend listening on port ${PORT}`));
