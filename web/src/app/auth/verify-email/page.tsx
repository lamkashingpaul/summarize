"use client";

import { Loader } from "@/components/loader";
import { AlertFailure } from "@/components/ui/alert-failure";
import { AlertSuccess } from "@/components/ui/alert-success";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useVerifyEmail } from "@/features/auth/api/use-verify-email";
import { VerifyEmailResponse } from "@/features/auth/types";
import { formatErrorMessage } from "@/lib/utils";
import { ReactQueryError } from "@/types";
import {
  ArrowRight,
  CheckCircle,
  FileText,
  RotateCcw,
  XCircle,
} from "lucide-react";
import Link from "next/link";
import { useQueryState } from "nuqs";
import { ReactNode, Suspense, useEffect } from "react";

export default function SuspenseVerifyEmailPage() {
  return (
    <Suspense>
      <VerifyEmailPage />
    </Suspense>
  );
}

function VerifyEmailPage() {
  const [token] = useQueryState("token", { defaultValue: "" });

  const {
    mutate: verifyEmail,
    data: verifyEmailData,
    status: verifyEmailStatus,
    error: verifyEmailError,
  } = useVerifyEmail();

  useEffect(() => {
    verifyEmail({ token });
  }, [verifyEmail, token]);

  if (verifyEmailStatus === "error") {
    return <VerifyEmailError error={verifyEmailError} />;
  }

  if (verifyEmailStatus === "success") {
    return <VerifyEmailSuccess data={verifyEmailData} />;
  }

  return <VerifyEmailLoader />;
}

function VerifyEmailPageWrapper({ children }: { children?: ReactNode }) {
  return (
    <section className="my-auto">
      <div className="container-wrapper !max-w-md">
        <div className="container">
          <div className="mb-8 text-center">
            <div className="mb-2 flex items-center justify-center gap-2">
              <FileText className="text-primary h-8 w-8" />
              <span className="text-2xl font-bold">Summarize</span>
            </div>
          </div>

          <Card>{children}</Card>
        </div>
      </div>
    </section>
  );
}

function VerifyEmailSuccess({ data }: { data: VerifyEmailResponse }) {
  const message = data?.detail;

  return (
    <VerifyEmailPageWrapper>
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
          <CheckCircle className="h-6 w-6 text-green-600" />
        </div>
        <CardTitle className="text-2xl font-bold">
          Email Verified Successfully!
        </CardTitle>
        {message ? <CardDescription>{message}</CardDescription> : null}
      </CardHeader>

      <CardContent className="space-y-4">
        <AlertSuccess
          icon={null}
          title={null}
          description="Your email has been successfully verified!"
        />

        <div className="bg-muted/30 mt-6 rounded-lg p-4">
          <h4 className="mb-2 text-sm font-medium">What&apos;s next?</h4>
          <ul className="text-muted-foreground list-inside list-disc space-y-1 text-xs">
            <li>Your account is now fully activated</li>
            <li>You can sign in and start using Summarize</li>
            <li>Explore AI-powered research paper summaries</li>
            <li>Ask questions about any paper with our chatbot</li>
          </ul>
        </div>

        <Button asChild className="w-full">
          <Link href="/auth/sign-in">
            Sign In to Your Account
            <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
        </Button>
      </CardContent>
    </VerifyEmailPageWrapper>
  );
}

function VerifyEmailError({ error }: { error: ReactQueryError | null }) {
  const errorMessage = formatErrorMessage(error);

  return (
    <VerifyEmailPageWrapper>
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
          <XCircle className="h-6 w-6 text-red-600" />
        </div>
        <CardTitle className="text-2xl font-bold">
          Verification Failed
        </CardTitle>
        <CardDescription>
          We couldn&apos;t verify your email address
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        <AlertFailure icon={null} title={null} description={errorMessage} />

        <div className="bg-muted/30 mt-6 rounded-lg p-4">
          <h4 className="mb-2 text-sm font-medium">Common causes:</h4>
          <ul className="text-muted-foreground list-inside list-disc space-y-1 text-xs">
            <li>The link may have been used already</li>
            <li>The link might be corrupted or incomplete</li>
            <li>The link may have expired</li>
          </ul>
        </div>

        <div className="space-y-2">
          <Button asChild className="w-full">
            <Link href="/auth/resend-verification">
              <RotateCcw className="mr-2 h-4 w-4" />
              Get New Verification Email
            </Link>
          </Button>
          <Button asChild variant="outline" className="w-full bg-transparent">
            <Link href="/auth/signin">Back to Sign In</Link>
          </Button>
        </div>

        <div className="text-muted-foreground text-center text-sm">
          <p>
            Still having trouble?{" "}
            <Link href="/contact" className="text-primary hover:underline">
              Contact support
            </Link>
          </p>
        </div>
      </CardContent>
    </VerifyEmailPageWrapper>
  );
}

function VerifyEmailLoader() {
  return (
    <VerifyEmailPageWrapper>
      <CardContent className="space-y-4">
        <div className="flex justify-center">
          <Loader />
        </div>
        <div className="space-y-2 text-center">
          <h3 className="text-lg font-semibold">Verifying your email...</h3>
          <p className="text-muted-foreground text-sm">
            Please wait while we confirm your email address.
          </p>
        </div>
      </CardContent>
    </VerifyEmailPageWrapper>
  );
}
