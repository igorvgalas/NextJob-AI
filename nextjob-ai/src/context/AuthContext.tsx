import { createContext, useContext } from "react";

export interface AuthResource {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
}

const AuthContext = createContext<AuthResource | null>(null);

export const ContextProvider = AuthContext.Provider;

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("AuthContext is not provided");
  return context;
};