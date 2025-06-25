// API route para login/logout via Discord OAuth2, integrando com backend FastAPI
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    // Redireciona para o endpoint de login do backend
    res.redirect(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/auth/login`);
  } else {
    res.status(405).end();
  }
}
