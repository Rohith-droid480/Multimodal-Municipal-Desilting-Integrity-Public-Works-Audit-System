import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'MuniAudit-AI — Municipal Public-Works Evidence Reconciliation Console',
  description: 'Multimodal municipal public-works evidence reconciliation and audit triage platform for municipal accounts officers and vigilance reviewers.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-app-bg text-slate-100 flex flex-col h-screen w-screen overflow-hidden antialiased">
        {children}
      </body>
    </html>
  );
}
