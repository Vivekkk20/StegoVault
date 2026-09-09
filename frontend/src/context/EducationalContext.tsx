import React, { createContext, useContext, useState, useEffect } from 'react';

interface EducationalContextType {
  isEduMode: boolean;
  toggleEduMode: () => void;
  setEduMode: (val: boolean) => void;
}

const EducationalContext = createContext<EducationalContextType | undefined>(undefined);

export const EducationalProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isEduMode, setIsEduMode] = useState<boolean>(() => {
    const saved = localStorage.getItem('stegovault_edu_mode');
    return saved !== null ? saved === 'true' : true; // Default ON for educational platform
  });

  useEffect(() => {
    localStorage.setItem('stegovault_edu_mode', String(isEduMode));
  }, [isEduMode]);

  const toggleEduMode = () => setIsEduMode(prev => !prev);
  const setEduMode = (val: boolean) => setIsEduMode(val);

  return (
    <EducationalContext.Provider value={{ isEduMode, toggleEduMode, setEduMode }}>
      {children}
    </EducationalContext.Provider>
  );
};

export const useEducational = () => {
  const context = useContext(EducationalContext);
  if (!context) {
    throw new Error('useEducational must be used within an EducationalProvider');
  }
  return context;
};
