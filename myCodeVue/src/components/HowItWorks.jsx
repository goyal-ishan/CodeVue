import './HowItWorks.css';
function HowItWorks() {
    return (
        <section id="how-it-works" className="how-it-works">

            <div className="how-it-works-header">
                
                <h2>How CodeVue Works</h2>

                <p>
                    Four structured phases mirroring real senior engineering
                    interview loops.
                </p>
            </div>

            <div className="workflow-cards">

                <div className="workflow-card">
                    <div className="card-top">
                        <span>01</span>
                        <span>⚙</span>
                    </div>

                    <h3>Prepare</h3>

                    <p>
                        Select topic (Data Structures, Algorithms,
                        System Design), target company difficulty
                        (Google, Meta, Amazon), and custom interviewer persona.
                    </p>

                    <a href="#">Customizable Rubrics →</a>
                </div>


                <div className="workflow-card">
                    <div className="card-top">
                        <span>02</span>
                        <span>♧</span>
                    </div>

                    <h3>Interview</h3>

                    <p>
                        Live AI interviewer asks clarifying questions,
                        introduces edge cases, and speaks naturally via
                        low-latency sub-second audio.
                    </p>

                    <a href="#">Conversational Speech →</a>
                </div>


                <div className="workflow-card">
                    <div className="card-top">
                        <span>03</span>
                        <span>&lt;&gt;</span>
                    </div>

                    <h3>Solve & Explain</h3>

                    <p>
                        Write executable code in a full sandbox IDE while
                        explaining your thought process and algorithmic
                        tradeoffs out loud.
                    </p>

                    <a href="#">Real Sandboxed Runtimes →</a>
                </div>


                <div className="workflow-card">
                    <div className="card-top">
                        <span>04</span>
                        <span>▣</span>
                    </div>

                    <h3>Get Feedback</h3>

                    <p>
                        Instant score breakdown on Problem Solving,
                        Code Quality, Speed, and Communication with
                        line-by-line critique.
                    </p>

                    <a href="#">FAANG Grading Rubric →</a>
                </div>

            </div>

        </section>
    );
}

export default HowItWorks;