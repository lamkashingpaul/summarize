import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { SignInForm } from "@/features/auth/components/sign-in-form";
import { SocialSignInForm } from "@/features/auth/components/social-sign-in-form";
import { ArrowLeft, FileText } from "lucide-react";
import Link from "next/link";

export default function SignInPage() {
  return (
    <section className="my-auto">
      <div className="container-wrapper !max-w-md">
        <div className="container">
          <div className="mb-8 text-center">
            <Link
              href="/"
              className="text-muted-foreground hover:text-foreground mb-6 inline-flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Summarize</span>
            </Link>
            <div className="mb-2 flex items-center justify-center gap-2">
              <FileText className="text-primary h-8 w-8" />
              <span className="text-2xl font-bold">Summarize</span>
            </div>
            <p className="text-muted-foreground">
              Create your account to get started
            </p>
          </div>
          <Card>
            <CardHeader className="space-y-1">
              <CardTitle className="text-center text-2xl font-bold">
                Sign In
              </CardTitle>
              <CardDescription className="text-center">
                Join thousands of researchers using AI to understand papers
                faster
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              <SocialSignInForm />

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <Separator className="w-full" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background text-muted-foreground px-2">
                    Or continue with email
                  </span>
                </div>
              </div>

              <SignInForm />

              <div className="text-center text-sm">
                <span className="text-muted-foreground">
                  Don&apos;t have an account?{" "}
                </span>
                <Link
                  href="/auth/sign-up"
                  className="text-primary font-medium hover:underline"
                >
                  Sign up
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
