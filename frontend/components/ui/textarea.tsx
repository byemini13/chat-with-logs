import * as React from "react";

export const Textarea = React.forwardRef<
  HTMLTextAreaElement,
  React.TextareaHTMLAttributes<HTMLTextAreaElement>
>(({ className, ...props }, ref) => {
  return (
    <textarea
      ref={ref}
      className={`border border-gray-300 rounded-md p-2 w-full focus:ring focus:ring-blue-300 ${className}`}
      {...props}
    />
  );
});

Textarea.displayName = "Textarea";
