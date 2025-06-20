import React from 'react';
import './Button.css';

export default function Button({ children, ...props }) {
  return (
    <button className="my-button" {...props}>
      {children}
    </button>
  );
}
