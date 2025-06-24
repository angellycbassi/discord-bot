import React from "react";

interface CampaignBannerProps {
  nome: string;
  bannerUrl?: string;
}

export default function CampaignBanner({ nome, bannerUrl }: CampaignBannerProps) {
  return (
    <div style={{
      width: "100%",
      minHeight: 180,
      borderRadius: 16,
      overflow: "hidden",
      marginBottom: 24,
      boxShadow: "0 4px 24px rgba(0,0,0,0.18)",
      position: "relative",
      background: bannerUrl ? `url(${bannerUrl}) center/cover no-repeat` : "var(--background-secondary)",
      display: "flex",
      alignItems: "flex-end",
    }}>
      <div style={{
        width: "100%",
        background: "rgba(0,0,0,0.45)",
        color: "#fff",
        padding: 16,
        fontSize: 28,
        fontWeight: 700,
        textShadow: "0 2px 8px #000",
      }}>
        {nome}
      </div>
    </div>
  );
}
