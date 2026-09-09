import { useState } from 'react';
import { EducationalProvider } from './context/EducationalContext';
import { Sidebar } from './components/common/Sidebar';
import { Header } from './components/common/Header';
import { Dashboard } from './pages/Dashboard';
import { EncodePage } from './pages/EncodePage';
import { DecodePage } from './pages/DecodePage';
import { AnalyzerPage } from './pages/AnalyzerPage';
import { ReportsPage } from './pages/ReportsPage';
import { SettingsPage } from './pages/SettingsPage';
import { AboutPage } from './pages/AboutPage';

export function App() {
  const [currentTab, setCurrentTab] = useState<string>('dashboard');
  const [reportTargetId, setReportTargetId] = useState<string | undefined>(undefined);

  const handleNavigate = (tab: string, reportId?: string) => {
    setReportTargetId(reportId);
    setCurrentTab(tab);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const getPageTitle = (tab: string) => {
    switch (tab) {
      case 'dashboard':
        return { title: 'Dashboard Overview', subtitle: 'Platform status and forensic operations' };
      case 'encode':
        return { title: 'Steganographic Encoding', subtitle: 'Authenticated AES-256-GCM data hiding' };
      case 'decode':
        return { title: 'Steganographic Decoding', subtitle: 'Payload extraction & cryptographic decryption' };
      case 'analyzer':
        return { title: 'Forensic Steganalysis Lab', subtitle: 'Statistical and structural image inspection' };
      case 'reports':
        return { title: 'Forensic Reports Repository', subtitle: 'Archived analysis telemetry & exports' };
      case 'settings':
        return { title: 'Platform Settings', subtitle: 'Educational mode & cryptographic baseline' };
      case 'about':
        return { title: 'About & Threat Model', subtitle: 'Cybersecurity theory and architecture' };
      default:
        return { title: 'StegoVault', subtitle: 'Educational Cybersecurity Platform' };
    }
  };

  const pageInfo = getPageTitle(currentTab);

  return (
    <EducationalProvider>
      <div className="flex min-h-screen bg-[#090d16] text-slate-100 selection:bg-cyan-500 selection:text-slate-950">
        {/* Navigation Sidebar */}
        <Sidebar currentTab={currentTab} onSelectTab={(tab) => handleNavigate(tab)} />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0">
          <Header title={pageInfo.title} subtitle={pageInfo.subtitle} />

          <main className="flex-1 p-8 overflow-y-auto max-w-7xl w-full mx-auto">
            {currentTab === 'dashboard' && <Dashboard onNavigate={handleNavigate} />}
            {currentTab === 'encode' && <EncodePage />}
            {currentTab === 'decode' && <DecodePage />}
            {currentTab === 'analyzer' && <AnalyzerPage />}
            {currentTab === 'reports' && <ReportsPage initialReportId={reportTargetId} />}
            {currentTab === 'settings' && <SettingsPage />}
            {currentTab === 'about' && <AboutPage />}
          </main>
        </div>
      </div>
    </EducationalProvider>
  );
}

export default App;
