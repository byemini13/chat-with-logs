import React from "react";
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";

export default function CodeSnippets({ snippets }: { snippets: { file: string; code: string }[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>File</TableHead>
          <TableHead>Snippet</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {snippets.map((snippet, index) => (
          <TableRow key={index}>
            <TableCell>{snippet.file}</TableCell>
            <TableCell>
              <pre className="text-xs">{snippet.code}</pre>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
