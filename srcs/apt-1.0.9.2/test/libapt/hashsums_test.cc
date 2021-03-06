#include <config.h>

#include <apt-pkg/md5.h>
#include <apt-pkg/sha1.h>
#include <apt-pkg/sha2.h>
#include <apt-pkg/strutl.h>
#include <apt-pkg/hashes.h>
#include <apt-pkg/fileutl.h>

#include <iostream>
#include <stdlib.h>
#include <string>

#include <gtest/gtest.h>

#include "file-helpers.h"

template <class T> void Test(const char *In,const char *Out)
{
   T Sum;
   Sum.Add(In);
   equals(Sum.Result().Value(), Out);
}



TEST(HashSumsTest,SummationStrings)
{
#define EXPECT_SUM(Summation, In, Out) \
   { \
      Summation Sum; \
      Sum.Add(In); \
      EXPECT_EQ(Sum.Result().Value(), Out) << #Summation << " for '" << In << "'"; \
   }

   // From  FIPS PUB 180-1
   EXPECT_SUM(SHA1Summation, "","da39a3ee5e6b4b0d3255bfef95601890afd80709");
   EXPECT_SUM(SHA1Summation, "abc","a9993e364706816aba3e25717850c26c9cd0d89d");
   EXPECT_SUM(SHA1Summation, "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
	 "84983e441c3bd26ebaae4aa1f95129e5e54670f1");

   // MD5 tests from RFC 1321
   EXPECT_SUM(MD5Summation, "","d41d8cd98f00b204e9800998ecf8427e");
   EXPECT_SUM(MD5Summation, "a","0cc175b9c0f1b6a831c399e269772661");
   EXPECT_SUM(MD5Summation, "abc","900150983cd24fb0d6963f7d28e17f72");
   EXPECT_SUM(MD5Summation, "message digest","f96b697d7cb7938d525a2f31aaf161d0");
   EXPECT_SUM(MD5Summation, "abcdefghijklmnopqrstuvwxyz","c3fcd3d76192e4007dfb496cca67e13b");
   EXPECT_SUM(MD5Summation, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
	 "d174ab98d277d9f5a5611c2c9f419d9f");
   EXPECT_SUM(MD5Summation, "12345678901234567890123456789012345678901234567890123456789012345678901234567890",
	 "57edf4a22be3c955ac49da2e2107b67a");

   // SHA-256, From FIPS 180-2
   EXPECT_SUM(SHA256Summation, "", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
   EXPECT_SUM(SHA256Summation, "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
	 "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1");

   // SHA-512
   EXPECT_SUM(SHA512Summation, "",
	 "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce"
	 "47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e");
   EXPECT_SUM(SHA512Summation, "abc",
	 "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a"
	 "2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f");


   EXPECT_SUM(MD5Summation, "The quick brown fox jumps over the lazy dog", "9e107d9d372bb6826bd81d3542a419d6");
   EXPECT_SUM(MD5Summation, "The quick brown fox jumps over the lazy dog.", "e4d909c290d0fb1ca068ffaddf22cbd0");
   EXPECT_SUM(SHA1Summation, "The quick brown fox jumps over the lazy dog", "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12");
   EXPECT_SUM(SHA1Summation, "The quick brown fox jumps over the lazy cog", "de9f2c7fd25e1b3afad3e85a0bd17d9b100db4b3");
   EXPECT_SUM(SHA256Summation, "The quick brown fox jumps over the lazy dog", "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592");
   EXPECT_SUM(SHA256Summation, "The quick brown fox jumps over the lazy dog.", "ef537f25c895bfa782526529a9b63d97aa631564d5d789c2b765448c8635fb6c");
   EXPECT_SUM(SHA512Summation, "The quick brown fox jumps over the lazy dog", "07e547d9586f6a73f73fbac0435ed76951218fb7d0c8d788a309d785436bbb64"
	 "2e93a252a954f23912547d1e8a3b5ed6e1bfd7097821233fa0538f3db854fee6");
   EXPECT_SUM(SHA512Summation, "The quick brown fox jumps over the lazy dog.", "91ea1245f20d46ae9a037a989f54f1f790f0a47607eeb8a14d12890cea77a1bb"
	 "c6c7ed9cf205e67b7f2b8fd4c7dfd3a7a8617e45f3c463d481c7e586c39ac1ed");

#undef EXPECT_SUM
}
TEST(HashSumsTest, Mill)
{
   SHA1Summation Sum1;

   const unsigned char As[] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
   size_t const AsCount = sizeof(As)/sizeof(As[0]) - 1;
   size_t Count = 1000000;
   while (Count != 0)
   {
      if (Count >= AsCount)
      {
	 Sum1.Add(As, AsCount);
	 Count -= AsCount;
      }
      else
      {
	 Sum1.Add(As,Count);
	 Count = 0;
      }
   }

   EXPECT_EQ("34aa973cd4c4daa4f61eeb2bdbad27316534016f", Sum1.Result().Value());
}

static void getSummationString(char const * const type, std::string &sum)
{
   /* to compare our result with an independent source we call the specific binaries
      and read their result back. We do this with a little trick by claiming that the
      summation is a compressor – and open the 'compressed' file later on directly to
      read out the summation sum calculated by it */
   APT::Configuration::Compressor compress(type, ".ext", type, NULL, NULL, 99);
   std::string name("apt-test-");
   name.append("hashsums").append(".XXXXXX");
   char * tempfile = strdup(name.c_str());
   int tempfile_fd = mkstemp(tempfile);
   close(tempfile_fd);
   ASSERT_NE(-1, tempfile_fd);

   FileFd fd;
   ASSERT_TRUE(fd.Open(tempfile, FileFd::WriteOnly | FileFd::Empty, compress));
   ASSERT_TRUE(fd.IsOpen());
   FileFd input(__FILE__, FileFd::ReadOnly);
   ASSERT_TRUE(input.IsOpen());
   ASSERT_NE(0, input.FileSize());
   ASSERT_TRUE(CopyFile(input, fd));
   ASSERT_TRUE(input.IsOpen());
   ASSERT_TRUE(fd.IsOpen());
   ASSERT_FALSE(fd.Failed());
   input.Close();
   fd.Close();
   ASSERT_TRUE(fd.Open(tempfile, FileFd::ReadOnly, FileFd::None));
   ASSERT_TRUE(fd.IsOpen());
   ASSERT_NE(0, fd.FileSize());
   ASSERT_FALSE(fd.Failed());
   unlink(tempfile);
   free(tempfile);
   char readback[2000];
   unsigned long long actual;
   ASSERT_TRUE(fd.Read(readback, sizeof(readback)/sizeof(readback[0]), &actual));
   actual -= 4;
   readback[actual] = '\0';
   sum = readback;
}
TEST(HashSumsTest, FileBased)
{
   std::string summation;

   getSummationString("md5sum", summation);
   MD5SumValue md5(summation);
   EXPECT_EQ(md5.Value(), summation);

   getSummationString("sha1sum", summation);
   SHA1SumValue sha1(summation);
   EXPECT_EQ(sha1.Value(), summation);

   getSummationString("sha256sum", summation);
   SHA256SumValue sha256(summation);
   EXPECT_EQ(sha256.Value(), summation);

   getSummationString("sha512sum", summation);
   SHA512SumValue sha512(summation);
   EXPECT_EQ(sha512.Value(), summation);

   FileFd fd(__FILE__, FileFd::ReadOnly);
   EXPECT_TRUE(fd.IsOpen());

   {
      Hashes hashes;
      hashes.AddFD(fd.Fd());
      EXPECT_EQ(md5.Value(), hashes.MD5.Result().Value());
      EXPECT_EQ(sha1.Value(), hashes.SHA1.Result().Value());
      EXPECT_EQ(sha256.Value(), hashes.SHA256.Result().Value());
      EXPECT_EQ(sha512.Value(), hashes.SHA512.Result().Value());
   }
   unsigned long sz = fd.FileSize();
   fd.Seek(0);
   {
      Hashes hashes;
      hashes.AddFD(fd.Fd(), sz);
      EXPECT_EQ(md5.Value(), hashes.MD5.Result().Value());
      EXPECT_EQ(sha1.Value(), hashes.SHA1.Result().Value());
      EXPECT_EQ(sha256.Value(), hashes.SHA256.Result().Value());
      EXPECT_EQ(sha512.Value(), hashes.SHA512.Result().Value());
   }
   fd.Seek(0);
   {
      MD5Summation MD5;
      MD5.AddFD(fd.Fd());
      EXPECT_EQ(md5.Value(), MD5.Result().Value());
   }
   fd.Seek(0);
   {
      SHA1Summation SHA1;
      SHA1.AddFD(fd.Fd());
      EXPECT_EQ(sha1.Value(), SHA1.Result().Value());
   }
   fd.Seek(0);
   {
      SHA256Summation SHA2;
      SHA2.AddFD(fd.Fd());
      EXPECT_EQ(sha256.Value(), SHA2.Result().Value());
   }
   fd.Seek(0);
   {
      SHA512Summation SHA2;
      SHA2.AddFD(fd.Fd());
      EXPECT_EQ(sha512.Value(), SHA2.Result().Value());
   }
   fd.Close();

   {
      HashString sha2("SHA256", sha256.Value());
      EXPECT_TRUE(sha2.VerifyFile(__FILE__));
   }
   {
      HashString sha2("SHA512", sha512.Value());
      EXPECT_TRUE(sha2.VerifyFile(__FILE__));
   }
   {
      HashString sha2("SHA256:" + sha256.Value());
      EXPECT_TRUE(sha2.VerifyFile(__FILE__));
   }
}
