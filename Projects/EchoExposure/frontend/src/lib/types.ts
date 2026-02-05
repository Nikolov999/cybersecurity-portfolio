export type Asset = {
  id: number;
  target: string;
  type: string;
  created_at: string;
};

export type Severity = "low" | "medium" | "high";

export type ServiceFinding = {
  port: number;
  service: string;
  severity: Severity;
};

export type ScanResult = {
  target: string;
  resolved_ip?: string;
  ports: number[];
  services: ServiceFinding[];
  risk_score: number;
  tags: string[];
};

export type Scan = {
  id: number;
  target: string;
  result: ScanResult;
  created_at: string;
};
