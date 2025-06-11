'use client';
import {
  GluestackUIProvider as Provider,
  StyledProvider,
} from '@gluestack-ui/themed';
import { config } from '@gluestack-ui/config';

export const GluestackUIProvider = ({
  children,
  mode,
}: {
  children: React.ReactNode;
  mode?: 'light' | 'dark' | null | undefined;
}) => {
  return (
    <StyledProvider config={config} colorMode={mode}>
      <Provider config={config} colorMode={mode}>
        {children}
      </Provider>
    </StyledProvider>
  );
};