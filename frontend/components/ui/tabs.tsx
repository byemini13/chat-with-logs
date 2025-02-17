import * as React from "react";

interface TabsProps {
  tabs: { id: string; label: string }[];
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export function Tabs({ tabs, activeTab, setActiveTab }: TabsProps) {
  return (
    <div>
      <div className="flex border-b">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`p-2 px-4 ${
              activeTab === tab.id ? "border-b-2 border-blue-600 font-semibold" : ""
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </div>
  );
}
