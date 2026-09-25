import Header from "../components/Header.jsx";
import InterviewSession from "../components/InterviewSession";
import HowItWorks from "../components/HowItWorks.jsx";
function Home(){
    return(
    <>  
        <Header/>

        <div className="Intro-Content">
            <h1 className="Intro">Practice Coding Interviews</h1>
            <h1 className="sub-Intro"> Like The Real Thing.</h1>
            <div className="description">
                <p>CodeView helps you prepare for coding interviews through realistic, AI-powered mock </p>
                <p>coding interviews with interactive voice prompts, real-time code evalutaion and </p>
                <p>actionable feedback.</p>
            </div>
            <button className="startMock">StartMock Interview </button>
        </div>
        <p className="Companies">Google Amazon Meta Netflix Stripe</p>
        <InterviewSession/>
        <HowItWorks/>
        
    </>
    );
}

export default Home;