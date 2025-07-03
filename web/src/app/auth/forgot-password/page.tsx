import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ForgotPasswordForm } from "@/features/auth/components/forgot-password-form";
import { ArrowLeft, FileText } from "lucide-react";
import Link from "next/link";

export default function ForgotPasswordPage() {
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
            <p className="text-muted-foreground">Reset your password</p>
          </div>

          <Card>
            <CardHeader className="space-y-1">
              <CardTitle className="text-center text-2xl font-bold">
                Forgot Password
              </CardTitle>
              <CardDescription className="text-center">
                Enter your email address and we&apos;ll send you a link to reset
                your password
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              <ForgotPasswordForm />

              <div className="text-center text-sm">
                <span className="text-muted-foreground">
                  Remember your password?{" "}
                </span>
                <Link
                  href="/auth/sign-in"
                  className="text-primary font-medium hover:underline"
                >
                  Sign in
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
