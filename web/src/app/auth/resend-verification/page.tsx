import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ResendVerificationForm } from "@/features/auth/components/resend-verification-form";
import { ArrowLeft, FileText } from "lucide-react";
import Link from "next/link";

export default function ResendVerificationPage() {
  return (
    <section className="my-auto">
      <div className="container-wrapper !max-w-md">
        <div className="container">
          <div className="mb-8 text-center">
            <Link
              href="/auth/sign-in"
              className="text-muted-foreground hover:text-foreground mb-6 inline-flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Sign In</span>
            </Link>
            <div className="mb-2 flex items-center justify-center gap-2">
              <FileText className="text-primary h-8 w-8" />
              <span className="text-2xl font-bold">Summarize</span>
            </div>
            <p className="text-muted-foreground">
              Resend your verification email
            </p>
          </div>

          <Card>
            <CardHeader className="space-y-1">
              <CardTitle className="text-center text-2xl font-bold">
                Resend Verification
              </CardTitle>
              <CardDescription className="text-center">
                Enter your email address and we&apos;ll send you a new
                verification link
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              <ResendVerificationForm />

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <Separator className="w-full" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background text-muted-foreground px-2">
                    other options
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <Button
                  asChild
                  variant="outline"
                  className="w-full bg-transparent text-sm"
                >
                  <Link href="/auth/sign-in">Try Sign In</Link>
                </Button>
                <Button
                  asChild
                  variant="outline"
                  className="w-full bg-transparent text-sm"
                >
                  <Link href="/auth/sign-up">Create Account</Link>
                </Button>
              </div>

              <div className="bg-muted/30 mt-6 rounded-lg p-4">
                <h4 className="mb-2 text-sm font-medium">Common Issues:</h4>
                <ul className="text-muted-foreground list-inside list-disc space-y-1 text-xs">
                  <li>Check your spam or junk folder</li>
                  <li>Make sure you&apos;re using the correct email address</li>
                  <li>Verification links expire after 1 hours</li>
                  <li>Some email providers may delay delivery</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
