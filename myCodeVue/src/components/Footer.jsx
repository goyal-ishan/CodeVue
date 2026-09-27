import React from 'react';
import { Code2, Activity, Share2, Globe } from 'lucide-react';
import './Footer.css';

function Footer() {
    return (
        <footer className="footer">

            <div className="footer-main">

                <div className="footer-brand">
                    <div className="footer-logo">
                        <Code2 size={18} />
                        <span>Code<span>Vue</span></span>
                    </div>

                    <p className="footer-description">
                        Master technical interviews with realistic, AI-powered mock coding environments.
                    </p>

                    <div className="footer-status">
                        <Activity size={12} />
                        <span>ALL SYSTEMS OPERATIONAL</span>
                    </div>
                </div>

            </div>

            <div className="footer-bottom">

                <p className="footer-copyright">
                    © 2025 CodeVue Inc. All rights reserved.
                </p>

                <div className="footer-icons">
                    <Share2 size={15} />
                    <Globe size={15} />
                </div>

            </div>

        </footer>
    );
}

export default Footer;