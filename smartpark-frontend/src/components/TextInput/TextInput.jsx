import React from 'react';
import './TextInput.css';

export default function TextInput({ value, onChange, placeholder, type = 'text', ...props }) {
  return (
    <input
      className="my-text-input"
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      {...props}
    />
  );
}
