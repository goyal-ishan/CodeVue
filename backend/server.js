require('dotenv').config();
const cors=require('cors');
const express=require('express');
const connectToDB=require('./database/db.js');
const authRoutes=require('./routers/auth-routes.js');

connectToDB();

const app=express();
app.use(cors({
  origin: [
    'http://localhost:5173',
    'https://codevue-frontend.onrender.com',
    process.env.FRONTEND_URL
  ].filter(Boolean),
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
const port=process.env.PORT||8080;

app.use(express.json());
app.use('/api/auth', authRoutes);


app.listen(port,()=>{
    console.log(`Server is listening on port ${port}`);
})

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', uptime: process.uptime() });
});