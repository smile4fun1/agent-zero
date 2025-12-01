import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Bot, Sparkles, Zap, Shield } from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <nav className="flex items-center justify-between mb-20">
          <div className="flex items-center space-x-2">
            <Bot className="h-8 w-8 text-primary" />
            <span className="text-2xl font-bold gradient-text">Agent Zero</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </nav>

        {/* Hero Content */}
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <div className="space-y-4">
            <h1 className="text-6xl font-bold tracking-tight">
              Enterprise AI Orchestration
              <br />
              <span className="gradient-text">Built for Scale</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Production-ready AI platform with customizable personas, 
              multi-agent orchestration, and domain-specific capabilities 
              for robotics, finance, engineering, and more.
            </p>
          </div>

          <div className="flex items-center justify-center space-x-4">
            <Link href="/register">
              <Button size="lg" className="group">
                Start Building
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            <Link href="/docs">
              <Button size="lg" variant="outline">
                View Documentation
              </Button>
            </Link>
          </div>

          {/* Demo Video/Screenshot Placeholder */}
          <div className="mt-12 rounded-lg border bg-card p-2">
            <div className="aspect-video rounded-md bg-muted flex items-center justify-center">
              <div className="text-center space-y-2">
                <Bot className="h-16 w-16 text-muted-foreground mx-auto" />
                <p className="text-muted-foreground">Dashboard Preview</p>
              </div>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="mt-32 grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <FeatureCard
            icon={<Sparkles className="h-6 w-6" />}
            title="Customizable Personas"
            description="Create AI agents with unique personalities, expertise, and behaviors tailored to your needs."
          />
          <FeatureCard
            icon={<Zap className="h-6 w-6" />}
            title="Real-time Streaming"
            description="Get instant responses with streaming support, live updates, and WebSocket communication."
          />
          <FeatureCard
            icon={<Shield className="h-6 w-6" />}
            title="Enterprise Ready"
            description="Built for production with authentication, rate limiting, monitoring, and scalable architecture."
          />
        </div>

        {/* Use Cases */}
        <div className="mt-32 max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">
            Built for Multiple Industries
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            <UseCaseCard
              title="Robotics Engineering"
              description="ROS development, motion planning, computer vision, and hardware integration for service robotics."
              tags={["ROS", "Computer Vision", "Motion Planning"]}
            />
            <UseCaseCard
              title="Financial Analysis"
              description="Market research, portfolio optimization, risk assessment, and quantitative analysis."
              tags={["Analysis", "Risk Management", "Reporting"]}
            />
            <UseCaseCard
              title="Software Engineering"
              description="Code generation, architecture design, code review, and best practices guidance."
              tags={["Development", "Architecture", "Review"]}
            />
            <UseCaseCard
              title="Marketing & Content"
              description="Content creation, SEO optimization, campaign planning, and analytics."
              tags={["Content", "SEO", "Analytics"]}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="glass rounded-lg p-6 space-y-4 hover:shadow-lg transition-shadow">
      <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
        {icon}
      </div>
      <h3 className="text-xl font-semibold">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  );
}

function UseCaseCard({
  title,
  description,
  tags,
}: {
  title: string;
  description: string;
  tags: string[];
}) {
  return (
    <div className="border rounded-lg p-6 space-y-4 hover:border-primary transition-colors">
      <h3 className="text-xl font-semibold">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
      <div className="flex flex-wrap gap-2">
        {tags.map((tag) => (
          <span
            key={tag}
            className="px-3 py-1 rounded-full bg-primary/10 text-primary text-sm"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}
