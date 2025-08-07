
import React from 'react';

const FormattedMessage = ({ text }) => {
  const parts = text.split(/(\*.*?\*)/g);

  return (
    <p className="whitespace-pre-wrap">
      {parts.filter(part => part).map((part, index) => {
        if (part.startsWith('*') && part.endsWith('*')) {
          return <strong key={index} className="text-blue-400 font-semibold">{part.slice(1, -1)}</strong>;
        }
        return part;
      })}
    </p>
  );
};

export default FormattedMessage;