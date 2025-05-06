// src/pages/Register.tsx

import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Link, useNavigate } from 'react-router-dom';

const Register = () => 
{
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async () => {
    setIsLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
      });

      if (res.ok) {
        navigate('/login');
      } else {
        alert('Erreur lors de l\'inscription.');
      }
    } catch (error) {
      console.error('Erreur lors de l\'inscription :', error);
      alert('Erreur lors de l\'inscription.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="glass p-8 rounded-2xl shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-semibold mb-6 text-center">Créer un compte</h1>
        <div className="space-y-4">
          <Input
            placeholder="Nom"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <Input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Input
            type="password"
            placeholder="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button
            className="w-full"
            onClick={handleRegister}
            disabled={isLoading}
          >
            {isLoading ? 'Création...' : "S'inscrire"}
          </Button>
        </div>
        <p className="mt-4 text-center text-sm text-muted-foreground">
          Déjà un compte ? <Link to="/login" className="text-primary underline">Se connecter</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
