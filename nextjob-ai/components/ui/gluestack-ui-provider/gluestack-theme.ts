import { createConfig } from '@gluestack-style/react';
import { config } from '@gluestack-ui/config';

export const gluestackConfig = createConfig({
  ...config, // або своя тема
  tokens: {
    colors: {
      backgroundDark950: '#121212',
      backgroundLight50: '#ffffff',
      textDark900: '#000000',
      textDark700: '#333333',
      textLight700: '#aaaaaa',
      textLight900: '#ffffff',
      borderLight300: '#d1d5db',
      primary500: '#3b82f6',
    },
  },
});