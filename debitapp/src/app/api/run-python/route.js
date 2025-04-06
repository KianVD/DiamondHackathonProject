import { exec } from "child_process";
import path from "path";
import { NextResponse } from "next/server";

export async function GET() {
  const scriptPath = path.join(process.cwd(), "scripts", "debit.py");

  return new Promise((resolve) => {
    exec(`python ${scriptPath}`, (error, stdout, stderr) => {
      if (error) {
        console.error("Python error:", stderr);
        return resolve(NextResponse.json({ error: stderr }, { status: 500 }));
      }
      return resolve(NextResponse.json({ output: stdout }));
    });
  });
}