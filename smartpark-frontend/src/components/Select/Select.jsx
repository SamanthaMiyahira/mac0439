import React from 'react';
import './Select.css';

export default function Select({ value, onChange, children, ...props }) {
  return (
    <select className="my-select" value={value} onChange={onChange} {...props}>
      {children}
    </select>
  );
}
