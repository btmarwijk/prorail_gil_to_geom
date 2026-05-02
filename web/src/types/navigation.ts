import { type ReactNode } from 'react';

export interface MenuItem {
  text: string;
  path: string;
  icon: ReactNode;
}