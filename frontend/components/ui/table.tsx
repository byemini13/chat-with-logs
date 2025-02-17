import * as React from "react";

interface TableProps {
  headers: string[];
  data: string[][];
}

export function Table({ headers, data }: TableProps) {
  return (
    <table className="w-full border-collapse border border-gray-300">
      <thead>
        <tr className="bg-gray-100">
          {headers.map((header, idx) => (
            <th key={idx} className="border p-2 text-left">{header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, rowIndex) => (
          <tr key={rowIndex} className="border">
            {row.map((cell, cellIndex) => (
              <td key={cellIndex} className="border p-2">{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
