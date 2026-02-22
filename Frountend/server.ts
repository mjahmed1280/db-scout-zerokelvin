import express from "express";
import { createServer as createViteServer } from "vite";
import path from "path";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API Mock Endpoints
  app.post("/api/database/test", (req, res) => {
    const { config } = req.body;
    console.log("Testing connection:", config);
    // Simulate successful connection
    setTimeout(() => {
      res.json({ status: "success", message: "Connection established successfully." });
    }, 1500);
  });

  app.get("/api/database/schemas", (req, res) => {
    console.log("Fetching schemas...");
    setTimeout(() => {
      res.json({
        status: "success",
        count: 4,
        schemas: [
          "public",
          "bikestore",
          "olist",
          "pg_toast-d"
        ]
      });
    }, 1000);
  });

  app.post("/api/analysis/run", (req, res) => {
    const { user_id, schema_name } = req.body;
    console.log("Running analysis for:", user_id, "Schemas:", schema_name);
    
    // Simulate long-running agentic process
    setTimeout(() => {
      res.json({
        status: "success",
        json_gcs_path: "dummy-->gs://db-scout-bucket/analysis_v1.json",
        md_gcs_path: "gs://db-scout-bucket/intelligence_docs.md",
        rag_corpus_id: "corpus_998877",
        preview_tables: Array.isArray(schema_name) 
          ? schema_name.flatMap(s => [`${s}.users`, `${s}.orders`])
          : [`${schema_name}.users`, `${schema_name}.orders`, "products", "inventory"]
      });
    }, 8000);
  });

  app.post("/api/chat", (req, res) => {
    const { query, rag_corpus_id, session_id } = req.body;
    console.log("Chat query:", query);
    
    setTimeout(() => {
      res.json({
        response: `Based on the scouted schema in **${rag_corpus_id}**, here is what I found:
        
The \`users\` table has a direct relationship with \`orders\` via \`user_id\`. 
There is a potential data anomaly in \`shipping_logs\` where 15% of entries lack a tracking number.

Would you like me to generate a SQL query to investigate the shipping logs further?`
      });
    }, 2000);
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static(path.resolve(__dirname, "dist")));
    app.get("*", (req, res) => {
      res.sendFile(path.resolve(__dirname, "dist", "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
