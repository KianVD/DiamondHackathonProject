'use client';

import { useState } from 'react';

export default function Home() {
  const [output, setOutput] = useState("");

  const runScript = async () => {
    const res = await fetch("/api/run-python");
    const data = await res.json();
    setOutput(data.output || data.error);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Debit Card Transaction Analyzer</h1>
      <button onClick={runScript} style={{ padding: "0.5rem 1rem" }}>
        Run Script
      </button>
      {output && (
        <pre style={{ marginTop: "1rem", background: "#f5f5f5", padding: "1rem" }}>
          {output}
        </pre>
      )}
    </div>
  );
}