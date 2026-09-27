require('dotenv').config();
const express=require('express');
const connectToDB=require('./database/db.js');
const authRoutes=require('./routers/auth-routes.js');
connectToDB();

const app=express();
const port=process.env.PORT||8080;

app.use(express.json());
app.use('/api/auth', authRoutes);


app.listen(port,()=>{
    console.log(`Server is listening on port ${port}`);
})