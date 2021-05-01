///////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2002, Industrial Light & Magic, a division of Lucas
// Digital Ltd. LLC
// 
// All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
// *       Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
// *       Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
// *       Neither the name of Industrial Light & Magic nor the names of
// its contributors may be used to endorse or promote products derived
// from this software without specific prior written permission. 
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
///////////////////////////////////////////////////////////////////////////



//-----------------------------------------------------------------------------
//
//	class CompressionAttribute
//
//-----------------------------------------------------------------------------

#include "ImfCompressionAttribute.h"


OPENEXR_IMF_INTERNAL_NAMESPACE_SOURCE_ENTER

using namespace OPENEXR_IMF_INTERNAL_NAMESPACE;


template <>
const char *
CompressionAttribute::staticTypeName ()
{
    return "compression";
}


template <>
void
CompressionAttribute::writeValueTo (OPENEXR_IMF_INTERNAL_NAMESPACE::OStream &os, int version) const
{
    unsigned char tmp = _value;
    Xdr::write <StreamIO> (os, tmp);
}


template <>
void
CompressionAttribute::readValueFrom (OPENEXR_IMF_INTERNAL_NAMESPACE::IStream &is, int size, int version)
{
    unsigned char tmp;
    Xdr::read <StreamIO> (is, tmp);

    //
    // prevent invalid values being written to Compressin enum
    // by forcing all unknown types to NUM_COMPRESSION_METHODS which is also an invalid
    // pixel type, but can be used as a PixelType enum value
    // (Header::sanityCheck will throw an exception when files with invalid Compression types are read)
    //

    if (tmp!= NO_COMPRESSION &&
      tmp != RLE_COMPRESSION &&
      tmp != ZIPS_COMPRESSION &&
      tmp != ZIP_COMPRESSION &&
      tmp != PIZ_COMPRESSION &&
      tmp != PXR24_COMPRESSION &&
      tmp != B44_COMPRESSION &&
      tmp != B44A_COMPRESSION &&
      tmp != DWAA_COMPRESSION &&
      tmp != DWAB_COMPRESSION)
    {
        tmp = NUM_COMPRESSION_METHODS;
    }

    _value = Compression (tmp);
}


OPENEXR_IMF_INTERNAL_NAMESPACE_SOURCE_EXIT 
