"use client";

import { signInSchema } from "@/features/auth/schemas/sign-in.schema";
import { SubmitHandler, useForm } from "react-hook-form";
import { z } from "zod/v4";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { InputWithAnEye } from "@/components/ui/input-with-an-eye";
import Link from "next/link";
import { useSignIn } from "@/features/auth/api/use-sign-in";
import { Checkbox } from "@/components/ui/checkbox";
import { formatErrorMessage } from "@/lib/utils";
import { AlertSuccess } from "@/components/ui/alert-success";
import { AlertFailure } from "@/components/ui/alert-failure";
import { ButtonWithLoading } from "@/components/ui/button-with-loading";
import { useEffect } from "react";

type SignInFormInput = z.input<typeof signInSchema>;
type SignInFormOutput = z.output<typeof signInSchema>;

export const SignInForm = () => {
  const {
    mutateAsync: signIn,
    data: signInData,
    isPending: isSignInPending,
  } = useSignIn();

  const form = useForm({
    defaultValues: getSignInFormDefaultValues,
    resolver: zodResolver(signInSchema),
    disabled: isSignInPending,
  });

  const {
    handleSubmit,
    control,
    setError,
    reset,
    formState: { errors, isSubmitSuccessful },
  } = form;

  const onSubmit: SubmitHandler<SignInFormOutput> = async (data) => {
    try {
      await signIn(data);
    } catch (error) {
      const errorMessage = formatErrorMessage(error);
      setError("root.serverError", { type: "server", message: errorMessage });
    }
  };

  useEffect(() => {
    if (isSubmitSuccessful) {
      reset();
    }
  }, [isSubmitSuccessful, reset]);

  return (
    <Form {...form}>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {signInData?.detail ? (
          <AlertSuccess
            title="Account Created"
            description={`${signInData.detail} Please check your email for verification instructions.`}
          />
        ) : null}

        {errors?.root?.serverError?.type === "server" ? (
          <AlertFailure
            title="Sign Up Failed"
            description={errors.root.serverError.message}
          />
        ) : null}

        <FormField
          control={control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="Enter your email" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <InputWithAnEye placeholder="Enter your password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex items-center justify-between">
          <FormField
            control={control}
            name="rememberMe"
            render={({ field }) => (
              <FormItem className="flex items-center space-x-2">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
                <FormLabel className="text-sm">Remember me</FormLabel>
              </FormItem>
            )}
          />

          <Link
            href="/auth/forgot-password"
            className="text-primary text-sm hover:underline"
          >
            Forgot password?
          </Link>
        </div>

        <ButtonWithLoading
          type="submit"
          className="w-full"
          isLoading={isSignInPending}
        >
          Sign In
        </ButtonWithLoading>
      </form>
    </Form>
  );
};

const getSignInFormDefaultValues = {
  email: "",
  password: "",
  rememberMe: false,
} satisfies SignInFormInput;
