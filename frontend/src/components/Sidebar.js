import React, { useState } from 'react';
import {
    FileText, Share2, Settings,
    ChevronDown, ChevronRight, ChevronUp,
    Github, Linkedin, Phone, Mail,
    Moon, Sun, Globe
} from 'lucide-react';
import { translations } from '../translations';
import './Sidebar.css';

const Sidebar = ({ isOpen, toggleTheme, theme, language, toggleLanguage }) => {
    const [expandedSections, setExpandedSections] = useState({
        cv: false,
        social: false,
        contact: false
    });
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);

    const toggleSection = (section) => {
        setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
    };

    const t = translations[language].sidebar;

    if (!isOpen) return null;

    return (
        <div className={`sidebar ${theme}`}>
            <div className="sidebar-header">
                <div className="profile-section">
                    <div className="profile-image-container">
                        {/* Place your profile photo in frontend/public/ and update the src below */}
                        <img src="/profile.png" alt="Profile" className="profile-image" />
                    </div>
                    <h3>{t.profileName}</h3>
                    <p className="profile-desc">{t.profileDesc}</p>
                </div>
            </div>

            <div className="sidebar-content">
                {/* CV Section */}
                <div className="sidebar-section">
                    <button className="section-header" onClick={() => toggleSection('cv')}>
                        <div className="section-title">
                            <FileText size={18} />
                            <span>{t.cv}</span>
                        </div>
                        {expandedSections.cv ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                    </button>
                    {expandedSections.cv && (
                        <div className="section-content">
                            {/* Place your CV PDFs in frontend/public/ and update the href below */}
                            <a href="/YOUR_CV_TR.pdf" target="_blank" rel="noopener noreferrer" className="sidebar-link">{t.turkceCv}</a>
                            <a href="/YOUR_CV_EN.pdf" target="_blank" rel="noopener noreferrer" className="sidebar-link">{t.englishCv}</a>
                        </div>
                    )}
                </div>

                {/* Social Media Section */}
                <div className="sidebar-section">
                    <button className="section-header" onClick={() => toggleSection('social')}>
                        <div className="section-title">
                            <Share2 size={18} />
                            <span>{t.socialMedia}</span>
                        </div>
                        {expandedSections.social ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                    </button>
                    {expandedSections.social && (
                        <div className="section-content">
                            {/* Replace with your own LinkedIn and GitHub URLs */}
                            <a href="https://www.linkedin.com/in/YOUR-LINKEDIN/" target="_blank" rel="noopener noreferrer" className="sidebar-link">
                                <Linkedin size={16} /> LinkedIn
                            </a>
                            <a href="https://github.com/YOUR-GITHUB" target="_blank" rel="noopener noreferrer" className="sidebar-link">
                                <Github size={16} /> GitHub
                            </a>
                        </div>
                    )}
                </div>

                {/* Contact Section */}
                <div className="sidebar-section">
                    <button className="section-header" onClick={() => toggleSection('contact')}>
                        <div className="section-title">
                            <Phone size={18} />
                            <span>{t.contact}</span>
                        </div>
                        {expandedSections.contact ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                    </button>
                    {expandedSections.contact && (
                        <div className="section-content">
                            {/* Replace with your email address */}
                            <div className="contact-item">
                                <Mail size={14} /> <span>your.email@example.com</span>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            <div className="sidebar-footer">
                {isSettingsOpen && (
                    <div className="settings-popover">
                        <button onClick={toggleTheme} className="setting-option">
                            {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
                            <span>{theme === 'dark' ? t.lightTheme : t.darkTheme}</span>
                        </button>
                        <button onClick={toggleLanguage} className="setting-option">
                            <Globe size={16} />
                            <span>{language === 'tr' ? 'English' : 'Türkçe'}</span>
                        </button>
                    </div>
                )}
                <button className="settings-btn" onClick={() => setIsSettingsOpen(!isSettingsOpen)}>
                    <div className="settings-label">
                        <Settings size={20} />
                        <span>{t.settings}</span>
                    </div>
                    {isSettingsOpen ? <ChevronDown size={16} /> : <ChevronUp size={16} />}
                </button>
            </div>
        </div>
    );
};

export default Sidebar;
